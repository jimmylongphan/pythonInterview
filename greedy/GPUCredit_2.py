"""
GPU Credits II

Each credit grant has a unique ID, an amount, and a valid half-open time
window: [timestamp, expiration_timestamp). Subtraction events permanently
consume credits from grants that are active at the subtraction timestamp.
When several grants are active, credits from the grant expiring soonest must
be used first.

Events may be received out of timestamp order. get_balance(timestamp) must
consider all events at or before the requested timestamp and process them in
chronological order. If a subtraction requests more credits than are
available, return None for that timestamp and every later timestamp.

Solution:
We store grant and subtraction events without immediately changing a balance.
For each query, we sort and replay all relevant events by timestamp. During a
subtraction, we find active grants, order them by expiration time, and consume
their remaining credits. Replaying from scratch makes the result depend on
event timestamps rather than the order in which the methods were called.

Step by step:
1. Build a timeline containing every grant and subtraction up to the query
   timestamp, then sort it chronologically.
2. Process each event in the timeline:
   - For a Grant, add a new GrantBalance to remaining_grants.
   - For a Subtraction, find the active grants and sort them by expiration.
     Consume the soonest-expiring grants until the subtraction reaches zero.
     If the active grants run out first, return None.
3. After replaying the timeline, start a separate result variable named
   balance at zero. Add the remaining credits from every grant that is still
   active at the query timestamp, then return balance. This does not reset the
   individual GrantBalance objects; it only totals their remaining credits.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Grant:
    """A grant event received by the system."""

    timestamp: int
    grant_id: str
    amount: int
    expiration_timestamp: int


@dataclass(frozen=True)
class Subtraction:
    """A subtraction event received by the system."""

    timestamp: int
    amount: int


@dataclass
class GrantBalance:
    """A grant's changeable balance while get_balance replays the timeline."""

    grant_id: str
    remaining: int
    expiration_timestamp: int


class CreditSystem:
    def __init__(self) -> None:
        # key: unique grant ID
        # value: Grant object containing all of the grant's information
        self._grants: dict[str, Grant] = {}

        self._subtractions: list[Subtraction] = []

        # The prompt guarantees unique event timestamps. Tracking them lets us
        # report accidental duplicate timestamps clearly.
        self._event_timestamps: set[int] = set()

    def create_grant(
        self,
        timestamp: int,
        grant_id: str,
        amount: int,
        expiration_timestamp: int,
    ) -> None:
        """Record a new grant active on [timestamp, expiration_timestamp)."""
        if grant_id in self._grants:
            raise ValueError(f"Grant ID already exists: {grant_id!r}")
        if amount <= 0:
            raise ValueError("Grant amount must be positive")
        if timestamp >= expiration_timestamp:
            raise ValueError("timestamp must be earlier than expiration_timestamp")
        self._claim_event_timestamp(timestamp)

        self._grants[grant_id] = Grant(
            timestamp=timestamp,
            grant_id=grant_id,
            amount=amount,
            expiration_timestamp=expiration_timestamp,
        )

    def subtract(self, timestamp: int, amount: int) -> None:
        """Record a request to permanently consume credits at timestamp."""
        if amount <= 0:
            raise ValueError("Subtraction amount must be positive")
        self._claim_event_timestamp(timestamp)

        self._subtractions.append(
            Subtraction(timestamp=timestamp, amount=amount)
        )

    def get_balance(self, timestamp: int) -> int | None:
        """Return remaining active credits, or None after an invalid subtraction."""
        timeline: list[Grant | Subtraction] = []

        # Add every grant that started by the query timestamp.
        for grant in self._grants.values():
            if grant.timestamp <= timestamp:
                timeline.append(grant)

        # Add every permanent subtraction that happened by the query timestamp.
        for subtraction in self._subtractions:
            if subtraction.timestamp <= timestamp:
                timeline.append(subtraction)

        # Method calls can arrive out of order, so put their objects into the
        # order in which they happened.
        timeline.sort(key=lambda event: event.timestamp)

        # This dictionary represents the state of each grant while we replay
        # the timeline.
        #
        # key: grant ID
        # value: GrantBalance object whose remaining amount can change
        remaining_grants: dict[str, GrantBalance] = {}

        # Replay one event at a time, from the earliest event to the latest.
        for event in timeline:
            # A grant event makes a new grant available. Nothing is consumed
            # yet, so its remaining credits begin at its original amount.
            if isinstance(event, Grant):
                remaining_grants[event.grant_id] = GrantBalance(
                    grant_id=event.grant_id,
                    remaining=event.amount,
                    expiration_timestamp=event.expiration_timestamp,
                )
                continue

            # If this is not a Grant, it is a Subtraction.
            # amount_needed tracks how much of this request is still unpaid.
            amount_needed = event.amount

            # Find grants that can pay for this subtraction. A grant is active
            # if it has credits left and has not expired at the subtraction's
            # timestamp.
            active_grants: list[GrantBalance] = []

            for grant_balance in remaining_grants.values():
                is_active = (
                    grant_balance.remaining > 0
                    and event.timestamp < grant_balance.expiration_timestamp
                )

                if is_active:
                    active_grants.append(grant_balance)

            # The prompt says to consume the soonest-expiring grant first.
            active_grants.sort(
                key=lambda grant_balance: (
                    grant_balance.expiration_timestamp,
                    grant_balance.grant_id,
                )
            )

            # Keep consuming active grants until this subtraction is fully
            # paid or there are no active grants left.
            for grant_balance in active_grants:
                # Use the smaller number:
                # - everything still needed by the subtraction, or
                # - everything available in this grant.
                amount_used = min(amount_needed, grant_balance.remaining)

                # Permanently reduce this grant's remaining credits.
                grant_balance.remaining -= amount_used

                # Reduce the unpaid part of the subtraction by the same amount.
                amount_needed -= amount_used

                if amount_needed == 0:
                    break

            # A positive amount means all active grants were exhausted before
            # the subtraction was fully paid. The timeline is invalid here,
            # so this query and all queries after this event return None.
            if amount_needed > 0:
                return None

        # All events were processed successfully. Add only grants that still
        # have credits and are active at the requested query timestamp.
        balance = 0

        for grant_balance in remaining_grants.values():
            is_active = (
                grant_balance.remaining > 0
                and timestamp < grant_balance.expiration_timestamp
            )

            if is_active:
                balance += grant_balance.remaining

        return balance

    def _claim_event_timestamp(self, timestamp: int) -> None:
        """Validate the prompt's requirement that every event timestamp is unique."""
        if timestamp in self._event_timestamps:
            raise ValueError(f"Event timestamp already exists: {timestamp}")
        self._event_timestamps.add(timestamp)


if __name__ == "__main__":
    # Example 1
    credits = CreditSystem()
    credits.create_grant(10, "a", 3, 60)
    credits.create_grant(20, "b", 2, 40)
    credits.subtract(30, 1)
    credits.subtract(50, 3)

    assert credits.get_balance(10) == 3
    assert credits.get_balance(20) == 5
    assert credits.get_balance(30) == 4
    assert credits.get_balance(40) == 3
    assert credits.get_balance(50) == 0
    assert credits.get_balance(60) == 0

    # Example 2: one subtraction consumes credits across multiple grants.
    credits = CreditSystem()
    credits.create_grant(10, "a", 3, 60)
    credits.create_grant(20, "b", 2, 80)
    credits.subtract(30, 4)

    assert credits.get_balance(10) == 3
    assert credits.get_balance(20) == 5
    assert credits.get_balance(30) == 1
    assert credits.get_balance(70) == 1

    # Example 3: a later grant cannot repair an earlier invalid subtraction.
    credits = CreditSystem()
    credits.create_grant(10, "a", 3, 60)
    credits.subtract(20, 4)
    credits.create_grant(40, "b", 10, 60)

    assert credits.get_balance(10) == 3
    assert credits.get_balance(20) is None
    assert credits.get_balance(50) is None

    # Events received out of chronological order.
    credits = CreditSystem()
    credits.subtract(30, 1)
    credits.create_grant(10, "a", 1, 100)

    assert credits.get_balance(10) == 1
    assert credits.get_balance(20) == 1
    assert credits.get_balance(30) == 0

    print("All tests passed.")

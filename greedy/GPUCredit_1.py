"""
GPU Credit System

You are designing a system to manage GPU credits. Each credit grant has a
unique ID and is valid during a specific time window. Credit grants may
overlap in time.

Because of network delays, events such as adding or consuming credits may
arrive and be processed out of order with respect to their timestamps. At any
time, you may query the system for the total available credits at a particular
timestamp or attempt to consume credits at a specified time.

Implement the CreditSystem class:

- CreditSystem()
  Initializes an empty credit system.

- grantCredit(id, amount, startTime, expirationTime)
  Adds a uniquely identified credit grant containing ``amount`` credits. The
  grant is active during the half-open interval [startTime, expirationTime):
  it is available at startTime but unavailable at expirationTime.

- subtract(amount, timestamp)
  Records that ``amount`` credits were consumed at ``timestamp``. The
  subtraction applies only at that exact timestamp and does not reduce later
  balances. It may be recorded before a grant covering that time is added.

- getBalance(timestamp)
  Returns all credits from grants active at ``timestamp``, minus all amounts
  subtracted at that exact timestamp. Returns -1 if deductions exceed the
  available credits.

Operations are processed in the order received, but balances must be
calculated according to each operation's timestamp.

Solution:
We keep two simple records: one for all credit grants and one for how many
credits were used at each exact timestamp. When getBalance(time) is called, we
look through the grants and add the ones that are active at that time. Then we
subtract only the credits used at that same time. We calculate the answer from
scratch on every query, so events can arrive in any order. For example, if a
subtraction arrives before its grant, the balance may first be -1; after the
grant arrives, the next query includes it and returns the correct balance.
"""

from collections import defaultdict


class CreditSystem:
    """Manage timestamped GPU credit grants and subtractions."""

    def __init__(self) -> None:
        # id -> (amount, start_time, expiration_time)
        self._grants: dict[str, tuple[int, int, int]] = {}
        # key: timestamp
        # value: total credits subtracted at that exact timestamp
        self._subtractions: defaultdict[int, int] = defaultdict(int)

    def grantCredit(
        self, id: str, amount: int, startTime: int, expirationTime: int
    ) -> None:
        """Add a uniquely identified grant active on [startTime, expirationTime)."""
        if id in self._grants:
            raise ValueError(f"Credit grant ID already exists: {id!r}")
        if amount < 0:
            raise ValueError("Credit amount cannot be negative")
        if startTime >= expirationTime:
            raise ValueError("startTime must be earlier than expirationTime")

        self._grants[id] = (amount, startTime, expirationTime)

    def subtract(self, amount: int, timestamp: int) -> None:
        """Record a subtraction that applies only at the exact timestamp."""
        if amount < 0:
            raise ValueError("Subtraction amount cannot be negative")

        self._subtractions[timestamp] += amount

    def getBalance(self, timestamp: int) -> int:
        """Return the available balance at timestamp, or -1 if overdrawn."""
        granted = sum(
            amount
            for amount, start_time, expiration_time in self._grants.values()
            if start_time <= timestamp < expiration_time
        )
        balance = granted - self._subtractions[timestamp]
        return balance if balance >= 0 else -1


if __name__ == "__main__":
    credit_system = CreditSystem()

    credit_system.grantCredit("a", 3, 10, 60)
    assert credit_system.getBalance(10) == 3

    credit_system.grantCredit("b", 2, 20, 40)
    credit_system.subtract(1, 30)
    credit_system.subtract(3, 50)

    expected_balances = {
        10: 3,
        20: 5,
        30: 4,
        35: 5,
        40: 3,
        50: 0,
    }
    for timestamp, expected in expected_balances.items():
        assert credit_system.getBalance(timestamp) == expected

    # Out-of-order subtraction: initially overdrawn, then covered by a grant.
    credit_system.subtract(4, 70)
    assert credit_system.getBalance(70) == -1
    credit_system.grantCredit("c", 5, 65, 75)
    assert credit_system.getBalance(70) == 1

    print("All tests passed.")

import copy
import heapq


class Transaction:
    def __init__(self, grant_id: str, amount: int, timestamp: int, expire: int):
        self.grant_id = grant_id # empty if subtraction
        self.amount = amount
        self.timestamp = timestamp
        self.expire = expire # empty if subtraction

    def __lt__(self, other):
        """
        sort 
        1. compare the expirations first
        2. if the other has expiration, then this is less
        3. if both have timestamp, then check it is subtraction, no grant
        4. compare timestamps
        """
        # addition, addition
        if self.expire is not None and other.expire is not None:
            return self.expire < other.expire
            
        # addition, subtraction
        if self.expire is not None and other.expire is None:
            return True

        # subtraction, addition
        if self.timestamp == other.timestamp:
            # addition is less
            return self.grant_id is not None

        # subtraction, subtraction
        return self.timestamp < other.timestamp
    
    def __repr__(self):
        return f"{self.grant_id}: {self.amount}"

    def __str__(self):
        return f"{self.grant_id}: {self.amount}"


class GPUCredit:
    def __init__(self):
        self.transactions = []

    def add(self, grant_id: str, amount: int, timestamp: int, expire: int):
        # additions have all info
        self.transactions.append(Transaction(grant_id, amount, timestamp, expire))

    def subtract(self, amount: int, timestamp: int):
        # subtractions only have 2
        self.transactions.append(Transaction(None, amount, timestamp, None))

    def get_balance(self, timestamp: int) -> int:
        balance = []

        # filter all of the transactions and filter by timestamp
        # make a deepcopy because we are modifying the credits
        filtered_transactions = list(filter(lambda transaction: transaction.timestamp <= timestamp, copy.deepcopy(self.transactions)))

        # sort transactions use the __lt__
        sorted_filtered_transactions = sorted(filtered_transactions)

        # use min_heap get the balance
        heapq.heapify(balance)
        for transaction in sorted_filtered_transactions:
            # push all the additions
            if transaction.grant_id is not None:
                heapq.heappush(balance, transaction)
            else:
                # handle subtractions
                subtract_amount = transaction.amount

                # need to handle the subtract amounts
                while subtract_amount > 0:
                    # get the credit expiring first
                    credit = heapq.heappop(balance)

                    # credit expired already, consume it
                    if credit.expire < transaction.timestamp:
                        continue

                    # subtract is greater, then we consume the credit
                    if subtract_amount >= credit.amount:
                        subtract_amount -= credit.amount
                    else:
                        # subtract is smaller, update the credit and push it back
                        credit.amount -= subtract_amount
                        heapq.heappush(balance, credit)
                        # subtract is completed
                        subtract_amount = 0

        # for all expired credits, remove them
        while balance and timestamp >= balance[0].expire:
            heapq.heappop(balance)

        # sum up all the remaining credits
        print(sum(map(lambda transaction: transaction.amount, balance)))
        return sum(map(lambda transaction: transaction.amount, balance))


gpu = GPUCredit()
gpu.subtract(4, 30)
gpu.get_balance(10) # value is None
gpu.add('a', 4, 20, 30)
gpu.get_balance(10) # value is 0
gpu.get_balance(20) # value is 4
print(gpu.get_balance(30)) # value is 0
 
gpu = GPUCredit()
gpu.add('a', 4, 20, 60)
gpu.add('b', 3, 30, 40)
gpu.subtract(2, 30)
gpu.get_balance(30) # value is 5
print(gpu.get_balance(40)) # value is 4

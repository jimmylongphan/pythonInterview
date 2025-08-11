
REBATE_DELAY_MS = 24 * 60 * 60 * 1000  # 24 hours in milliseconds

class Account:
    def __init__(self, username, balance=0):
        self.username = username
        self.balance = float(balance)
        self.pending_rebates = []  # List of (rebate_amount, rebate_timestamp)

    def _execute_rebates(self, current_timestamp):
        # each rebate is a tuple (rebate_amount, rebate_timestamp)
        # Apply rebates whose scheduled time is <= current_timestamp
        rebates_to_apply = [r for r in self.pending_rebates if r[1] <= current_timestamp]
        for rebate_amount, rebate_timestamp in rebates_to_apply:
            self.balance += rebate_amount
            print(f"Rebate of {rebate_amount:.2f} applied at {rebate_timestamp}")
        # Remove applied rebates
        self.pending_rebates = [r for r in self.pending_rebates if r[1] > current_timestamp]

    def deposit(self, amount, timestamp=None):
        amount = float(amount)
        self._execute_rebates(timestamp)
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        print(f"{amount} deposited. New balance: {self.balance} (timestamp: {timestamp})")

    def withdraw(self, amount, timestamp=None):
        amount = float(amount)
        self._execute_rebates(timestamp)
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        print(f"{amount} withdrawn. New balance: {self.balance} (timestamp: {timestamp})")

    def get_balance(self, timestamp=None):
        self._execute_rebates(timestamp)
        return self.balance

    def schedule_rebate(self, rebate_amount, rebate_timestamp):
        self.pending_rebates.append((float(rebate_amount), rebate_timestamp))
        print(f"Rebate of {rebate_amount:.2f} scheduled for {rebate_timestamp}")

class BankingSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self, username, initial_deposit=0, timestamp=None):
        if username in self.accounts:
            raise ValueError("Account already exists.")
        self.accounts[username] = Account(username, initial_deposit)
        print(f"Account created for {username} with balance {initial_deposit} (timestamp: {timestamp})")

    def deposit(self, username, amount, timestamp=None):
        if username not in self.accounts:
            raise ValueError("Account does not exist.")
        self.accounts[username].deposit(amount, timestamp)

    def withdraw(self, username, amount, timestamp=None):
        if username not in self.accounts:
            raise ValueError("Account does not exist.")
        self.accounts[username].withdraw(amount, timestamp)

    def get_balance(self, username, timestamp=None):
        if username not in self.accounts:
            raise ValueError("Account does not exist.")
        return self.accounts[username].get_balance(timestamp)

    def pay(self, username, amount, timestamp):
        if username not in self.accounts:
            raise ValueError("Account does not exist.")
        account = self.accounts[username]
        account._execute_rebates(timestamp)
        if amount <= 0:
            raise ValueError("Pay amount must be positive.")
        if amount > account.balance:
            raise ValueError("Insufficient funds.")
        account.balance -= amount
        print(f"{amount} paid. New balance: {account.balance} (timestamp: {timestamp})")
        # Schedule 2% rebate for 24 hours later
        rebate_amount = amount * 0.02
        rebate_timestamp = timestamp + REBATE_DELAY_MS
        account.schedule_rebate(rebate_amount, rebate_timestamp)

if __name__ == "__main__":
    bank = BankingSystem()
    bank.create_account("Alice", 100, timestamp=1234567890123)
    bank.deposit("Alice", 50, timestamp=1234567891123)
    bank.pay("Alice", 30, timestamp=1234567892123)
    # Simulate time passing for rebate
    print("Alice's balance before rebate:", bank.get_balance("Alice", timestamp=1234567893123))
    print("Alice's balance after rebate:", bank.get_balance("Alice", timestamp=1234567892123 + REBATE_DELAY_MS))

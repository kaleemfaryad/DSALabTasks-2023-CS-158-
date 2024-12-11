class CashFlowMinimizer:
    def __init__(self):
        self.transactions = []  # List of (borrower, lender, amount)
        self.balances = {}

    def add_transaction(self, from_person, to_person, amount):
        self.transactions.append((from_person, to_person, amount))
        self.balances[from_person] = self.balances.get(from_person, 0) - amount
        self.balances[to_person] = self.balances.get(to_person, 0) + amount

    def minimize_cash_flow(self):
        # Step 1: Separate debtors and creditors
        debtors = []
        creditors = []
        for person, balance in self.balances.items():
            if balance < 0:
                debtors.append((person, abs(balance)))
            elif balance > 0:
                creditors.append((person, balance))

        # Step 2: Match debtors with creditors
        transactions_to_settle = []
        i, j = 0, 0
        while i < len(debtors) and j < len(creditors):
            debtor, debt = debtors[i]
            creditor, credit = creditors[j]

            transfer_amount = min(debt, credit)
            transactions_to_settle.append((debtor, creditor, transfer_amount))

            # Update balances
            debtors[i] = (debtor, debt - transfer_amount)
            creditors[j] = (creditor, credit - transfer_amount)

            if debtors[i][1] == 0:
                i += 1
            if creditors[j][1] == 0:
                j += 1

        return transactions_to_settle

    def display_transactions(self, transactions_to_settle):
        for transaction in transactions_to_settle:
            print(f"{transaction[0]} owes {transaction[1]}: {transaction[2]} units.")


# Example usage:
cfm = CashFlowMinimizer()
cfm.add_transaction('A', 'B', 100)
cfm.add_transaction('B', 'C', 50)
cfm.add_transaction('C', 'A', 150)

transactions_to_settle = cfm.minimize_cash_flow()
cfm.display_transactions(transactions_to_settle)

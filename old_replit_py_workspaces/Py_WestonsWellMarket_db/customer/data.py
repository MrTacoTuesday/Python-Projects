from datetime import date
from typing import Any, List

from .transaction import Transaction


class Data:

    def __init__(self,
                 balance: int,
                 dob: date,
                 transactions: List[Transaction] = []):
        self.balance = balance
        self.dob = dob
        self.transactions = transactions

    def __str__(self):
        _tr = '\n\t\t'.join(str(t) for t in self.transactions)
        return f"""\tBalance: {self.balance}, 
    DOB: {self.dob},
    Transaction History: {"Empty" if _tr == "" else _tr}"""

    def jsonify_data(self) -> dict[str, Any]:
        return {
            "balance": str(self.balance),
            "dob": self.dob.isoformat(),
            "transactions": (t.jsonify_data() for t in self.transactions)
        }

    @staticmethod
    def parse_json(data: dict[str, Any]) -> "Data":
        if not isinstance(data["transactions"], list):
            raise ValueError("Transactions must be a list")
        return Data(balance=int(data["balance"]),
                    dob=date.fromisoformat(data["dob"]),
                    transactions=[
                        Transaction.parse_json(_dat)
                        for _dat in data["transactions"]
                    ])

from datetime import datetime
from typing import Any

from research_tests_simulations.old_replit_py_workspaces.Py_WestonsWellMarket_db.customer.transaction import Transaction
from research_tests_simulations.old_replit_py_workspaces.Py_WestonsWellMarket_db.market import Services, getDiscountFx

from .data import Data


class Customer:

    def __init__(self, name: str, data: Data):
        self.name = name
        self.data = data

    def __str__(self):
        return f"Name: {self.name}: [\n{self.data}\n]"

    def purchaseService(self,
                        svcId: str,
                        minutes: int = 0,
                        byol: bool = False,
                        byom: bool = False):
        price = getDiscountFx(svcId,
                              birthday=self.data.dob,
                              byol=byol,
                              byom=byom)(minutes)
        if price == 0:
            raise ValueError(f"Service {svcId} not available")
        if self.data.balance < price:
            raise Exception(f"Insufficient balance: {self.data.balance}")
        self.data.balance -= price
        self.data.transactions.append(
            Transaction(price, datetime.today(), Services[svcId].name))
        print(f"Completed purchase of {{{Services[svcId].name}}}")

    def addBalance(self, amount: int):
        self.data.balance += amount
        print(f"Increased balance by {amount}")

    def removeBalance(self, amount: int):
        self.data.balance -= amount
        print(f"Decreased balance by {amount}")

    def checkBalance(self):
        print(f"Balance: {self.data.balance}")

    def checkTransactions(self):
        print("Transaction History:")
        for t in self.data.transactions:
            print(f"\t{t}")

    def viewDetails(self):
        print(self)

    def jsonify_data(self) -> dict[str, Any]:
        return {"name": self.name, "data": self.data.jsonify_data()}

    @staticmethod
    def parse_json(data: dict[str, Any]) -> "Customer":
        if not isinstance(data["data"], dict):
            raise ValueError("Transactions must be a dictionary")
        return Customer(data["name"], Data.parse_json(data["data"]))

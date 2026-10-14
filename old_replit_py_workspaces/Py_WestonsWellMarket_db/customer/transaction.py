from datetime import datetime


class Transaction:

    def __init__(self, expense: int, date: datetime, description: str):
        self.expense = expense
        self.date = date
        self.description = description

    def __str__(self):
        return f"{self.date}: {self.expense}WD ({self.description})"

    def jsonify_data(self) -> dict[str, str]:
        return {
            "expense": str(self.expense),
            "date": self.date.isoformat(),
            "description": self.description
        }

    @staticmethod
    def parse_json(data: dict[str, str]) -> "Transaction":
        return Transaction(expense=int(data["expense"]),
                           date=datetime.fromisoformat(data["date"]),
                           description=data["description"])

from datetime import date

from research_tests_simulations.old_replit_py_workspaces.Py_WestonsWellMarket_db.customer import Customer, Data
from research_tests_simulations.old_replit_py_workspaces.Py_WestonsWellMarket_db.files import loadCustomers, saveCustomers

CUSTOMERS = loadCustomers()
print(CUSTOMERS)
if "Heidi Chaney" not in CUSTOMERS:
    CUSTOMERS["Heidi Chaney"] = Customer("Heidi Chaney",
                                         Data(balance=50, dob=date(1981, 1, 2)))
print(CUSTOMERS)
print()
for name, customer in CUSTOMERS.items():
    print(f"Selected customer '{name}'")
    print(str(customer))
#saveCustomers(CUSTOMERS)

#### TO-DO::::
"""
- [x] Create a Customer class
- [x] Create Customer Json conversions
- [_] Create CLI for customer interaction
- [x] Fix save and load of encrypted customer json
"""

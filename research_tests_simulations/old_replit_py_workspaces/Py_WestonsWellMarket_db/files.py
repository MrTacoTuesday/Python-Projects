import json
from typing import Any, Dict

from research_tests_simulations.old_replit_py_workspaces.Py_WestonsWellMarket_db.customer import Customer


def loadCustomersJson() -> Dict[str, Dict[str, Any]]:
    with open("./data/customers", "r") as file:
        customers = bytes.fromhex(file.read()).decode('utf-8')
        return json.loads(customers)


def loadCustomers() -> Dict[str, Customer]:
    customersJSON = loadCustomersJson()
    return {
        name: Customer.parse_json(data)
        for name, data in customersJSON.items()
    }


def saveCustomersJson(customers: Dict[str, Dict[str, Any]]) -> None:
    with open("./data/customers", "w") as file:
        file.flush()
        cust = json.dumps(customers)
        #writes base64 encoding of cust to file
        file.write(bytes(cust, 'utf-8').hex())


def saveCustomers(customers: Dict[str, Customer]) -> None:
    saveCustomersJson({
        name: customer.jsonify_data()
        for name, customer in customers.items()
    })

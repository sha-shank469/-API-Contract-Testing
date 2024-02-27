import atexit
import unittest
from pact import Consumer, Provider,Pact
import requests
import os

# Define the Pact Consumer and Provider
pact = Consumer('Consumer').has_pact_with(Provider('Employee'))
pact.start_service()
atexit.register(pact.stop_service)


class GetEmployeeInfoContract(unittest.TestCase):
    """
    Test case class for validating the contract to retrieve information of a single employee by ID.
    """

    def test_get_employee(self):
        """
        Test method to validate the contract for retrieving information of a single employee by ID.
        """
        # Test data and expected response
        expected = {
            'id': 1,
            'name': 'John Doe',
            'age': 30,
            'department': 'IT'
        }

        # Define the interaction between Consumer and Provider using Pact
        (pact
            .given('Employee with ID 1 exists')
            .upon_receiving('a request for Employee with ID 1')
            .with_request('get', '/employees/1')
            .will_respond_with(200, body=expected))

        with pact:
            result = requests.get(pact.uri+'/employees/1').json()

        # Assert the response matches the expected result
        self.assertEqual(
            result, expected, f"Actual response: {result}, Expected response: {expected}")

        pact.verify()


class GetEmployeesInfoContract(unittest.TestCase):
    """
    Test case class for validating the contract to retrieve information of all employees.
    """

    def test_get_employees(self):
        """
        Test method to validate the contract for retrieving information of all employees.
        """
        # Test data and expected response
        expected = [{"id": 1, "name": "John Doe", "age": 30, "department": "IT"}, {
            "id": 2, "name": "Jane Smith", "age": 35, "department": "HR"}]

        # Define the interaction between Consumer and Provider using Pact
        (pact
            .upon_receiving('a request for all employees')
            .with_request('get', '/employees')
            .will_respond_with(201, body=expected))

        with pact:
            result = requests.get(pact.uri+'/employees').json()

        # Assert the response matches the expected result
        self.assertEqual(
            result, expected, f"Act ual response: {result}, Expected response: {expected}")

        pact.verify()


class CreateEmployeesInfoContract(unittest.TestCase):
    """
    Test case class for validating the contract to create a new employee entry.
    """

    def test_create_employee(self):
        """
        Test method to validate the contract for creating a new employee entry.
        """
        # Test data and expected response
        expected_request = {
            'id': 3,
            'name': 'John Smith',
            'age': 25,
            'department': 'Marketing'
        }
        expected_response = {
            'id': 3,
            'name': 'John Smith',
            'age': 25,
            'department': 'Marketing'
        }

        # Define the interaction between Consumer and Provider using Pact
        (pact
            .given('Employee creation is successful')
            .upon_receiving('a request to create an employee')
            .with_request('post', '/employees', body=expected_request)
            .will_respond_with(200, body=expected_response))

        with pact:
            result = requests.post(pact.uri+'/employees',
                                   json=expected_request).json()
            print("PACT URI",pact.uri)

        # Assert the response matches the expected result
        self.assertEqual(
            result, expected_response, f"Actual response: {result}, Expected response: {expected_response}")
        pact.verify()


class UpdateEmployeeInfoContract(unittest.TestCase):
    """
    Test case class for validating the contract to update information of an existing employee by ID.
    """

    def test_update_employee(self):
        """
        Test method to validate the contract for updating information of an existing employee by ID.
        """
        # Test data and expected response
        employee_id = 1
        expected_request = {
            'name': 'Shashank',
            'age': 25,
            'department': 'IT'
        }
        expected_response = {
            'id': employee_id,
            'name': 'Shashank',
            'age': 25,
            'department': 'IT'
        }

        # Define the interaction between Consumer and Provider using Pact
        (pact
            .given(f'Employee with ID {employee_id} exists')
            .upon_receiving(f'a request to update employee with ID {employee_id}')
            .with_request('put', f'/employees/{employee_id}', body=expected_request)
            .will_respond_with(200, body=expected_response))

        with pact:
            result = requests.put(
                f"{pact.uri}/employees/{employee_id}", json=expected_request).json()

        # Assert the response matches the expected result
        self.assertEqual(
            result, expected_response, f"Actual response: {result}, Expected response: {expected_response}")
        
        pact.verify()

        
# Execute the test cases if this script is executed directly
if __name__ == '__main__':
    unittest.main()
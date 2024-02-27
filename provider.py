"""
provider.py

This script defines a FastAPI application serving as the Provider for the contract tests defined in consumer.py.
The Provider offers endpoints for managing employee information, including retrieval, creation, and updating.

Endpoints:
    - GET /employees: Retrieve information for all employees.
    - POST /employees: Create a new employee entry.
    - GET /employees/{id}: Retrieve information for a specific employee by ID.
    - PUT /employees/{id}: Update information for a specific employee by ID.

Usage:
    Run this script directly to start the FastAPI server serving as the Provider.
"""

from pact.provider import Provider  # Import Provider class from the pact library
from fastapi import FastAPI  # Import FastAPI for building the API application

# Initialize a FastAPI application
app = FastAPI()

# Define a list of employee data as a placeholder database
employees = [
    {"id": 1, "name": "John Doe", "age": 30, "department": "IT"},
    {"id": 2, "name": "Jane Smith", "age": 35, "department": "HR"},
]

# Define endpoint to retrieve information for all employees
@app.get("/employees", response_model=list)
async def get_employees():
    return employees

# Define endpoint to create a new employee entry
@app.post("/employees", response_model=dict)
async def create_employee(employee: dict):
    employees.append(employee)
    return employee

# Define endpoint to retrieve information for a specific employee by ID
@app.get("/employees/{id}", response_model=dict)
async def get_employee(id: int):
    for emp in employees:
        if emp["id"] == id:
            return emp
    return {"message": "Employee not found"}

# Define endpoint to update information for a specific employee by ID
@app.put("/employees/{id}", response_model=dict)
async def update_employee(id: int, employee: dict):
    for emp in employees:
        if emp["id"] == id:
            emp.update(employee)
            return emp
    return {"message": "Employee not found"}

# Initialize the Provider with the name 'Employee'
provider = Provider('Employee')

# Run the FastAPI application if this script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="localhost", port=1234)

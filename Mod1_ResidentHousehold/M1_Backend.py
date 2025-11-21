# ----------------------------------------
# Install dependencies first if you haven't already:
# pip install fastapi uvicorn pydantic mysql-connector-python
# ----------------------------------------

# Import necessary libraries

from fastapi import FastAPI, HTTPException
# FastAPI: Framework to create APIs in Python easily
# HTTPException: Used to return error messages like 404 or 500

from pydantic import BaseModel, Field
# Pydantic: Used for validating data coming from users
# BaseModel: Base class to define data structure for validation
# Field: Allows setting default values or factory functions

from typing import Optional, List
# Optional: Marks a field as optional (can be None)
# List: Used to define list of items as type hint

import mysql.connector
# mysql.connector: Library to connect Python to MySQL database

from uuid import uuid4
# uuid4: Generates unique ID for each household automatically

from datetime import datetime
# datetime: Work with date and time values

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
db = mysql.connector.connect(
    host="localhost",       # Database is running on your computer
    user="root",            # MySQL username
    password="your_password", # Replace with your MySQL password
    database="resitrack"    # Name of the database we created
)

# Create a cursor object to execute SQL queries
cursor = db.cursor(dictionary=True)
# dictionary=True makes query results return as Python dictionaries
# Example: {'id': 'abc123', 'name': 'Juan', 'address': '123 Rizal St'}

# -----------------------------
# INITIALIZE FASTAPI APP
# -----------------------------
app = FastAPI()
# This creates the API server object

# -----------------------------
# DEFINE HOUSEHOLD DATA MODEL (VALIDATION)
# -----------------------------
class Household(BaseModel):
    # id: Unique ID, automatically generated using uuid4
    id: str = Field(default_factory=lambda: str(uuid4()))

    # name: Full name of the household head/resident
    name: str

    # address: Full address of the household
    address: str

    # latitude: GPS latitude of the household (decimal number)
    latitude: float

    # longitude: GPS longitude of the household (decimal number)
    longitude: float

    # contact: Optional phone number or email
    contact: Optional[str] = None

    # special_needs: Optional info for elderly, pregnant, disabled, etc.
    special_needs: Optional[str] = None

    # status: Safety status (default is 'unverified')
    status: str = "unverified"

    # created_at: Timestamp when record is created (optional, DB sets default)
    created_at: Optional[datetime] = None

    # updated_at: Timestamp when record is updated (optional, DB handles)
    updated_at: Optional[datetime] = None

# -----------------------------
# CREATE HOUSEHOLD (POST)
# -----------------------------
@app.post("/households", response_model=Household)
def create_household(household: Household):
    """
    This endpoint is used to create/add a new household in the database.
    Steps:
    1. Validate input using Pydantic (FastAPI does this automatically)
    2. Prepare SQL INSERT query
    3. Execute query and save to MySQL
    4. Return the created household data
    """
    sql = """
        INSERT INTO households
        (id, name, address, latitude, longitude, contact, special_needs, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    # %s placeholders will be replaced with actual values to prevent SQL injection

    values = (
        household.id,
        household.name,
        household.address,
        household.latitude,
        household.longitude,
        household.contact,
        household.special_needs,
        household.status
    )

    try:
        cursor.execute(sql, values)  # Run SQL query
        db.commit()  # Save changes permanently in database
        return household  # Return the created household data to frontend
    except Exception as e:
        # If anything goes wrong, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# READ ALL HOUSEHOLDS (GET)
# -----------------------------
@app.get("/households", response_model=List[Household])
def get_households():
    """
    This endpoint retrieves all households from the database.
    Steps:
    1. Execute SELECT query
    2. Fetch results as list of dictionaries
    3. Return the list to frontend
    """
    cursor.execute("SELECT * FROM households")  # Fetch all rows
    results = cursor.fetchall()  # Returns list of dicts
    # Example: [{'id': 'abc123', 'name': 'Juan', ...}, {...}]
    return results

# -----------------------------
# UPDATE HOUSEHOLD (PUT)
# -----------------------------
@app.put("/households/{household_id}", response_model=Household)
def update_household(household_id: str, updated: Household):
    """
    Update household data by ID
    Steps:
    1. Check if the household exists in DB
    2. If exists, update the record with new values
    3. Return the updated household data
    """
    # Check existence
    cursor.execute("SELECT * FROM households WHERE id=%s", (household_id,))
    existing = cursor.fetchone()
    if not existing:
        raise HTTPException(status_code=404, detail="Household not found")

    # Prepare SQL UPDATE query
    sql = """
        UPDATE households
        SET name=%s, address=%s, latitude=%s, longitude=%s,
            contact=%s, special_needs=%s, status=%s, updated_at=NOW()
        WHERE id=%s
    """
    values = (
        updated.name,
        updated.address,
        updated.latitude,
        updated.longitude,
        updated.contact,
        updated.special_needs,
        updated.status,
        household_id
    )

    try:
        cursor.execute(sql, values)  # Execute update
        db.commit()  # Save changes
        return updated  # Return updated household data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# DELETE HOUSEHOLD (DELETE)
# -----------------------------
@app.delete("/households/{household_id}")
def delete_household(household_id: str):
    """
    Delete a household by ID
    Steps:
    1. Check if the household exists
    2. If exists, delete it from DB
    3. Return success message
    """
    cursor.execute("SELECT * FROM households WHERE id=%s", (household_id,))
    existing = cursor.fetchone()
    if not existing:
        raise HTTPException(status_code=404, detail="Household not found")

    try:
        cursor.execute("DELETE FROM households WHERE id=%s", (household_id,))
        db.commit()  # Save deletion
        return {"message": "Household deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===============================
# Install dependencies if needed:
# pip install fastapi uvicorn pydantic mysql-connector-python
# ===============================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
import mysql.connector  # 🔹 Allows Python to connect and talk to MySQL
from uuid import uuid4   # 🔹 Generates unique IDs automatically
from datetime import datetime, timezone  # 🔹 For timestamps

# ===============================
# 1️⃣ Connect to MySQL database
# ===============================
# 🔹 host="localhost" → MySQL server is on your own computer
# 🔹 user="root" → MySQL username
# 🔹 password="your_password" → replace with your MySQL password
# 🔹 database="resitrack" → the database that stores your tables
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="resitrack"
)

# 🔹 Cursor is how Python sends SQL queries and gets results
# 🔹 dictionary=True → each row will be a Python dictionary (easier to read)
cursor = db.cursor(dictionary=True)

# ===============================
# 2️⃣ Initialize FastAPI app
# ===============================
# 🔹 This creates our API server
# 🔹 All routes (like GET, POST, PUT) will be defined on this app
app = FastAPI()

# ===============================
# 3️⃣ Define Incident model using Pydantic
# ===============================
class Incident(BaseModel):
    # 🔹 Pydantic validates incoming data automatically
    id: str = Field(default_factory=lambda: str(uuid4()))
    # 🔹 Automatically generate a unique ID (UUID) for each incident

    type: str  
    # 🔹 Type of disaster: "earthquake", "flood", "typhoon", etc.

    phase: str = "incoming"  
    # 🔹 Stage of disaster: "incoming" (warning), "occurring" (happening), "past" (over)

    severity: str  
    # 🔹 Danger level: "low", "medium", "high", "critical"

    description: str  
    # 🔹 Detailed info about the incident

    affected_area: str  
    # 🔹 Location impacted by disaster

    affected_families: int = 0  
    # 🔹 Start at 0, update as reports come in

    relief_distributed: int = 0  
    # 🔹 Track how many families have received aid

    created_at: Optional[datetime] = None  
    # 🔹 Timestamp when incident is created

    updated_at: Optional[datetime] = None  
    # 🔹 Timestamp when incident is last updated

# ===============================
# 4️⃣ CREATE Incident endpoint
# ===============================
@app.post("/incidents", response_model=Incident)
def create_incident(incident: Incident):
    # 🔹 This function runs when frontend sends POST /incidents
    # 🔹 Input is automatically validated as Incident model

    # 🔹 SQL query to insert data into MySQL table
    sql = """
        INSERT INTO incidents
        (id, type, phase, severity, description, affected_area, affected_families, relief_distributed, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
    """
    # 🔹 %s placeholders → safe way to insert values (avoids SQL injection)

    values = (
        incident.id,
        incident.type,
        incident.phase,
        incident.severity,
        incident.description,
        incident.affected_area,
        incident.affected_families,
        incident.relief_distributed
    )

    try:
        cursor.execute(sql, values)  # 🔹 Run the SQL command
        db.commit()  # 🔹 Save changes permanently to MySQL
        return incident  # 🔹 Return the incident data to frontend
    except Exception as e:
        # 🔹 If something goes wrong, send 500 Internal Server Error
        raise HTTPException(status_code=500, detail=str(e))

# ===============================
# 5️⃣ READ All Incidents endpoint
# ===============================
@app.get("/incidents", response_model=List[Incident])
def get_incidents():
    # 🔹 Triggered when frontend calls GET /incidents
    cursor.execute("SELECT * FROM incidents")  # 🔹 Get all rows from table
    results = cursor.fetchall()  # 🔹 Returns a list of dictionaries
    return results  # 🔹 Send this list to frontend

# ===============================
# 6️⃣ UPDATE Incident endpoint
# ===============================
@app.put("/incidents/{incident_id}", response_model=Incident)
def update_incident(incident_id: str, updated: Incident):
    # 🔹 Triggered when frontend calls PUT /incidents/{incident_id}
    # 🔹 Frontend sends the updated incident info

    # 1️⃣ Check if incident exists
    cursor.execute("SELECT * FROM incidents WHERE id=%s", (incident_id,))
    existing = cursor.fetchone()  # 🔹 Get the existing record
    if not existing:
        raise HTTPException(status_code=404, detail="Incident not found")  
        # 🔹 Return 404 if not found

    # 2️⃣ Prepare SQL UPDATE command
    sql = """
        UPDATE incidents
        SET type=%s, phase=%s, severity=%s, description=%s,
            affected_area=%s, affected_families=%s, relief_distributed=%s,
            updated_at=NOW()
        WHERE id=%s
    """
    values = (
        updated.type,
        updated.phase,
        updated.severity,
        updated.description,
        updated.affected_area,
        updated.affected_families,
        updated.relief_distributed,
        incident_id
    )

    try:
        cursor.execute(sql, values)  # 🔹 Run the UPDATE command
        db.commit()  # 🔹 Save changes
        return updated  # 🔹 Send updated incident to frontend
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===============================
# 7️⃣ DELETE Incident endpoint
# ===============================
@app.delete("/incidents/{incident_id}")
def delete_incident(incident_id: str):
    # 🔹 Triggered when frontend calls DELETE /incidents/{incident_id}

    # 1️⃣ Check if incident exists
    cursor.execute("SELECT * FROM incidents WHERE id=%s", (incident_id,))
    existing = cursor.fetchone()
    if not existing:
        raise HTTPException(status_code=404, detail="Incident not found")

    try:
        cursor.execute("DELETE FROM incidents WHERE id=%s", (incident_id,))
        db.commit()  # 🔹 Save changes
        return {"message": "Incident deleted successfully"}  # 🔹 Confirmation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

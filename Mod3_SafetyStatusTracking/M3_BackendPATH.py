@api_router.patch("/households/{household_id}/status")
async def toggle_status(household_id: str, status: str):
    """
    PATCH endpoint = partial update (only changes `status`)
    PUT would replace the whole household — we don't want that.
    """

    # ---------------------------------------------
    # 1) Check if household exists
    # ---------------------------------------------
    query = "SELECT status FROM households WHERE id = %s"
    async with db.connection.cursor() as cursor:
        await cursor.execute(query, (household_id,))
        row = await cursor.fetchone()

    if not row:
        # Household does not exist in database
        raise HTTPException(status_code=404, detail="Household not found")

    previous_status = row[0]  # Get the current status

    # ---------------------------------------------
    # 2) Insert into status_history (audit trail)
    # ---------------------------------------------
    history_query = """
        INSERT INTO status_history (household_id, previous_status, new_status)
        VALUES (%s, %s, %s)
    """

    async with db.connection.cursor() as cursor:
        await cursor.execute(history_query, (household_id, previous_status, status))
        await db.connection.commit()

    # ---------------------------------------------
    # 3) Update the household's status
    # ---------------------------------------------
    update_query = """
        UPDATE households
        SET status = %s, updated_at = NOW()
        WHERE id = %s
    """

    async with db.connection.cursor() as cursor:
        await cursor.execute(update_query, (status, household_id))
        await db.connection.commit()

    # ---------------------------------------------
    # 4) Fetch updated record to send back
    # ---------------------------------------------
    get_query = "SELECT id, name, address, status, updated_at FROM households WHERE id = %s"

    async with db.connection.cursor() as cursor:
        await cursor.execute(get_query, (household_id,))
        updated = await cursor.fetchone()

    # ---------------------------------------------
    # 5) Broadcast update to all connected clients
    # ---------------------------------------------
    await manager.broadcast({
        "type": "status_changed",
        "data": {
            "id": updated[0],
            "name": updated[1],
            "address": updated[2],
            "status": updated[3],
            "updated_at": str(updated[4])
        }
    })

    return {
        "message": "Status updated",
        "household": {
            "id": updated[0],
            "name": updated[1],
            "address": updated[2],
            "status": updated[3],
            "updated_at": str(updated[4])
        }
    }

@api_router.get("/metrics")
async def get_metrics():
    """
    Returns real-time dashboard statistics.
    """

    async with db.connection.cursor() as cursor:

        # Count ALL households
        await cursor.execute("SELECT COUNT(*) FROM households")
        total_households = (await cursor.fetchone())[0]

        # SAFE
        await cursor.execute("SELECT COUNT(*) FROM households WHERE status = 'safe'")
        safe_count = (await cursor.fetchone())[0]

        # NOT SAFE
        await cursor.execute("SELECT COUNT(*) FROM households WHERE status = 'not_safe'")
        not_safe_count = (await cursor.fetchone())[0]

        # UNVERIFIED
        await cursor.execute("SELECT COUNT(*) FROM households WHERE status = 'unverified'")
        unverified_count = (await cursor.fetchone())[0]

        # Percentage
        safe_percentage = (safe_count / total_households * 100) if total_households > 0 else 0

        # ACTIVE INCIDENTS
        await cursor.execute("""
            SELECT COUNT(*) FROM incidents
            WHERE phase IN ('incoming', 'occurring')
        """)
        active_incidents = (await cursor.fetchone())[0]

    return {
        "total_households": total_households,
        "safe_count": safe_count,
        "not_safe_count": not_safe_count,
        "unverified_count": unverified_count,
        "safe_percentage": round(safe_percentage, 1),
        "active_incidents": active_incidents
    }

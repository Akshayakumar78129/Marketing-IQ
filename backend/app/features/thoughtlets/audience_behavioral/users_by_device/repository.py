"""
Users by Device Type repository - Data access layer for device type metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class UsersByDeviceRepository:
    """Repository for users by device type data access operations."""

    @staticmethod
    def get_users_by_device(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch user counts by device category.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with device_category and users
        """
        date_conditions = []
        params = {}

        if date_from:
            date_conditions.append("DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            date_conditions.append("DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        date_filter = ""
        if date_conditions:
            date_filter = "WHERE " + " AND ".join(date_conditions)

        query = f"""
            SELECT
                DEVICE_CATEGORY,
                SUM(USERS) AS USERS
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_DEVICE_BROWSER
            {date_filter}
            GROUP BY DEVICE_CATEGORY
            ORDER BY USERS DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
users_by_device_repository = UsersByDeviceRepository()

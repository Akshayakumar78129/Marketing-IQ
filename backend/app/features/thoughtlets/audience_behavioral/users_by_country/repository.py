"""
Users by Country repository - Data access layer for country metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class UsersByCountryRepository:
    """Repository for users by country data access operations."""

    @staticmethod
    def get_users_by_country(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch user counts by country.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with country and users
        """
        date_conditions = ["GEO_LEVEL = 'country'"]
        params = {}

        if date_from:
            date_conditions.append("DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            date_conditions.append("DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        date_filter = "WHERE " + " AND ".join(date_conditions)

        query = f"""
            SELECT
                LOCATION_VALUE AS COUNTRY,
                SUM(USERS) AS USERS
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_GEO
            {date_filter}
            GROUP BY LOCATION_VALUE
            ORDER BY USERS DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
users_by_country_repository = UsersByCountryRepository()

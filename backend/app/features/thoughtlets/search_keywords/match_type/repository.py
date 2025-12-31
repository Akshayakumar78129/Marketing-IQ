"""
Search & Keywords Match Type repository - Data access layer for match type metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class MatchTypeRepository:
    """Repository for match type data access operations."""

    @staticmethod
    def get_match_type_distribution(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch keyword count and spend by match type.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with match type distribution data
        """
        date_conditions = []
        params = {}

        if date_from:
            date_conditions.append("f.DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            date_conditions.append("f.DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        date_filter = ""
        if date_conditions:
            date_filter = "AND " + " AND ".join(date_conditions)

        query = f"""
            SELECT
                k.MATCH_TYPE,
                COUNT(DISTINCT f.KEYWORD_ID) AS KEYWORD_COUNT,
                SUM(f.SPEND) AS SPEND
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_KEYWORD_PERFORMANCE f
            JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_KEYWORD k
                ON f.KEYWORD_ID = k.KEYWORD_ID AND k.IS_CURRENT = TRUE
            WHERE f.PLATFORM = 'google_ads'
                {date_filter}
            GROUP BY k.MATCH_TYPE
            ORDER BY SPEND DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
match_type_repository = MatchTypeRepository()

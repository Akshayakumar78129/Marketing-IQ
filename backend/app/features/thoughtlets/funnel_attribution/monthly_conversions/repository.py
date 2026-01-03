"""
Monthly Conversions repository - Data access layer for monthly conversion metrics.
"""
from datetime import date
from typing import Optional, List
from app.core.database import execute_query


class MonthlyConversionsRepository:
    """Repository for monthly conversions data access operations."""

    @staticmethod
    def get_monthly_conversions(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> List[dict]:
        """
        Fetch conversions aggregated by month.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with month and conversions
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
                TO_CHAR(DATE_DAY, 'Mon YYYY') AS MONTH,
                TO_CHAR(DATE_TRUNC('month', DATE_DAY), 'YYYY-MM') AS MONTH_SORT,
                ROUND(SUM(CONVERSIONS), 2) AS CONVERSIONS
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE
            {date_filter}
            GROUP BY TO_CHAR(DATE_DAY, 'Mon YYYY'), TO_CHAR(DATE_TRUNC('month', DATE_DAY), 'YYYY-MM')
            ORDER BY MONTH_SORT
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
monthly_conversions_repository = MonthlyConversionsRepository()

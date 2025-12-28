"""
Thoughtlets Core Performance Revenue vs Spend repository - Data access layer.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class RevenueVsSpendRepository:
    """Repository for revenue vs spend data access operations."""

    @staticmethod
    def get_revenue_vs_spend(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch monthly revenue and spend data.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with monthly revenue and spend data
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
                TO_CHAR(DATE_TRUNC('MONTH', DATE_DAY), 'Mon YYYY') AS MONTH,
                SUM(CONVERSION_VALUE) AS REVENUE,
                SUM(SPEND) AS SPEND
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE
            {date_filter}
            GROUP BY DATE_TRUNC('MONTH', DATE_DAY)
            ORDER BY DATE_TRUNC('MONTH', DATE_DAY)
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
revenue_vs_spend_repository = RevenueVsSpendRepository()

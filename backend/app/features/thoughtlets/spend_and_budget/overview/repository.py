"""
Thoughtlets Spend and Budget Overview repository - Data access layer for spend/budget metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class SpendAndBudgetOverviewRepository:
    """Repository for spend and budget overview data access operations across all platforms."""

    @staticmethod
    def get_overview(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> dict:
        """
        Fetch aggregated spend and budget metrics across all platforms.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            Dictionary with aggregated spend and budget metrics
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
                ROUND(SUM(SPEND), 2) AS TOTAL_SPEND,
                ROUND(SUM(CONVERSION_VALUE), 2) AS TOTAL_REVENUE,
                ROUND(SUM(CONVERSION_VALUE) / NULLIF(SUM(SPEND), 0), 3) AS OVERALL_ROAS,
                ROUND(SUM(SPEND) / NULLIF(SUM(CONVERSIONS), 0), 2) AS COST_PER_CONVERSION,
                ROUND(SUM(SPEND) / NULLIF(SUM(CLICKS), 0), 2) AS AVG_CPC,
                ROUND(SUM(SPEND) / NULLIF(COUNT(DISTINCT DATE_DAY), 0), 2) AS AVG_DAILY_SPEND,
                SUM(IMPRESSIONS) AS TOTAL_IMPRESSIONS,
                ROUND(SUM(CONVERSIONS), 0) AS CONVERSIONS
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE
            {date_filter}
        """

        results = execute_query(query, params if params else None)
        return results[0] if results else {}


# Singleton instance for dependency injection
spend_and_budget_overview_repository = SpendAndBudgetOverviewRepository()

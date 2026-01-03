"""
Thoughtlets Spend and Budget - Spend by Campaign repository - Data access layer.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class SpendByCampaignRepository:
    """Repository for spend by campaign data access operations."""

    @staticmethod
    def get_spend_by_campaign(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        platform: Optional[str] = None,
        status: Optional[str] = None
    ) -> list[dict]:
        """
        Fetch spend by campaign with filters.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            platform: Optional platform filter
            status: Optional status filter

        Returns:
            List of campaign data
        """
        conditions = ["1=1"]
        params = {}

        if date_from:
            conditions.append("DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            conditions.append("DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        if platform:
            conditions.append("PLATFORM = %(platform)s")
            params["platform"] = platform

        if status:
            conditions.append("STATUS = %(status)s")
            params["status"] = status

        where_clause = " AND ".join(conditions)

        query = f"""
            SELECT
                CAMPAIGN_NAME AS CAMPAIGN,
                PLATFORM,
                STATUS,
                SUM(SPEND) AS SPEND,
                SUM(CONVERSION_VALUE) AS REVENUE,
                SUM(CONVERSION_VALUE) / NULLIF(SUM(SPEND), 0) AS ROAS,
                SUM(CONVERSIONS) AS CONVERSIONS,
                SUM(SPEND) / NULLIF(SUM(CLICKS), 0) AS CPC
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE
            WHERE {where_clause}
            GROUP BY CAMPAIGN_NAME, PLATFORM, STATUS
            ORDER BY SPEND DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
spend_by_campaign_repository = SpendByCampaignRepository()

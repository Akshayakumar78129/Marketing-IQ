"""
Creative & Messaging - Impressions by Campaign repository - Data access layer.
"""
from datetime import date
from typing import Optional, List
from app.core.database import execute_query


class ImpressionsByCampaignRepository:
    """Repository for impressions by campaign data access operations."""

    @staticmethod
    def get_impressions_by_campaign(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 10
    ) -> List[dict]:
        """
        Fetch top campaigns by impressions for bar chart.

        Args:
            date_from: Optional start date for filtering
            date_to: Optional end date for filtering
            limit: Maximum number of campaigns to return (default 10)

        Returns:
            List of dictionaries with campaign_name and impressions
        """
        date_conditions = []
        params = {"limit": limit}

        if date_from:
            date_conditions.append("date_day >= %(date_from)s::DATE")
            params["date_from"] = date_from.isoformat()

        if date_to:
            date_conditions.append("date_day <= %(date_to)s::DATE")
            params["date_to"] = date_to.isoformat()

        date_filter = ""
        if date_conditions:
            date_filter = "AND " + " AND ".join(date_conditions)

        query = f"""
            SELECT
                campaign_name AS CAMPAIGN_NAME,
                SUM(impressions) AS IMPRESSIONS
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE
            WHERE platform = 'meta'
            {date_filter}
            GROUP BY campaign_name
            ORDER BY IMPRESSIONS DESC
            LIMIT %(limit)s
        """

        results = execute_query(query, params)
        return results if results else []


# Singleton instance for dependency injection
impressions_by_campaign_repository = ImpressionsByCampaignRepository()

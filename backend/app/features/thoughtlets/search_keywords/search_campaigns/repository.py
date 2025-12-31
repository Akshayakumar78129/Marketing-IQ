"""
Search & Keywords - Search Campaigns Performance repository - Data access layer.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class SearchCampaignsRepository:
    """Repository for search campaigns performance data access operations."""

    @staticmethod
    def get_search_campaigns(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch search campaign performance metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with search campaign performance data
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
                c.CAMPAIGN_NAME AS CAMPAIGN,
                c.CAMPAIGN_TYPE AS TYPE,
                c.STATUS,
                SUM(f.IMPRESSIONS) AS IMPRESSIONS,
                SUM(f.CLICKS) AS CLICKS,
                ROUND(SUM(f.CLICKS) * 100.0 / NULLIF(SUM(f.IMPRESSIONS), 0), 1) AS CTR,
                SUM(f.SPEND) AS SPEND,
                SUM(f.CONVERSIONS) AS CONVERSIONS,
                ROUND(SUM(f.CONVERSION_VALUE) / NULLIF(SUM(f.SPEND), 0), 2) AS ROAS
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE f
            JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_CAMPAIGN c
                ON f.CAMPAIGN_ID = c.CAMPAIGN_ID AND c.IS_CURRENT = TRUE
            WHERE f.PLATFORM = 'google_ads'
                AND c.CAMPAIGN_TYPE IN ('SEARCH', 'PERFORMANCE_MAX', 'SHOPPING')
                {date_filter}
            GROUP BY c.CAMPAIGN_NAME, c.CAMPAIGN_TYPE, c.STATUS
            ORDER BY IMPRESSIONS DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
search_campaigns_repository = SearchCampaignsRepository()

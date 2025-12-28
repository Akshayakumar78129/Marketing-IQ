"""
Meta Ads Campaigns repository - Data access layer for campaign metrics.
"""
from datetime import date
from typing import Optional, List
from app.core.database import execute_query


class MetaAdsCampaignsRepository:
    """Repository for Meta Ads campaigns data access operations."""

    @staticmethod
    def get_campaigns(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        status: Optional[str] = None
    ) -> List[dict]:
        """
        Fetch Meta Ads campaigns with aggregated metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            status: Optional campaign status filter

        Returns:
            List of dictionaries with campaign metrics
        """
        # Build filter conditions
        conditions = []
        params = {}

        if date_from:
            conditions.append("DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            conditions.append("DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        if status:
            conditions.append("STATUS = %(status)s")
            params["status"] = status.upper()

        # Build filter clause
        filter_clause = ""
        if conditions:
            filter_clause = "AND " + " AND ".join(conditions)

        query = f"""
            SELECT
                CAMPAIGN_ID,
                CAMPAIGN_NAME,
                STATUS,
                SUM(SPEND) AS TOTAL_SPEND,
                SUM(IMPRESSIONS) AS TOTAL_IMPRESSIONS,
                SUM(CLICKS) AS TOTAL_CLICKS,
                COALESCE(SUM(CONVERSIONS), 0) AS TOTAL_CONVERSIONS,
                COALESCE(SUM(CONVERSION_VALUE), 0) AS TOTAL_REVENUE,
                CASE WHEN SUM(SPEND) > 0 THEN COALESCE(SUM(CONVERSION_VALUE), 0) / SUM(SPEND) ELSE 0 END AS ROAS,
                CASE WHEN SUM(IMPRESSIONS) > 0 THEN (SUM(CLICKS) / SUM(IMPRESSIONS)) * 100 ELSE 0 END AS CTR,
                CASE WHEN SUM(CLICKS) > 0 THEN SUM(SPEND) / SUM(CLICKS) ELSE 0 END AS CPC,
                CASE WHEN SUM(IMPRESSIONS) > 0 THEN (SUM(SPEND) / SUM(IMPRESSIONS)) * 1000 ELSE 0 END AS CPM
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE
            WHERE PLATFORM = 'meta'
                {filter_clause}
            GROUP BY CAMPAIGN_ID, CAMPAIGN_NAME, STATUS
            ORDER BY TOTAL_SPEND DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
meta_ads_campaigns_repository = MetaAdsCampaignsRepository()

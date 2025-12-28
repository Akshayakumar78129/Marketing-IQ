"""
Meta Ads Ad Sets repository - Data access layer for ad set metrics.
"""
from datetime import date
from typing import Optional, List
from app.core.database import execute_query


class MetaAdsAdSetRepository:
    """Repository for Meta Ads ad set data access operations."""

    @staticmethod
    def get_ad_sets(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        ad_set_id: Optional[str] = None
    ) -> List[dict]:
        """
        Fetch Meta Ads ad set metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            ad_set_id: Optional ad set ID filter

        Returns:
            List of dictionaries with ad set metrics
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

        if ad_set_id:
            conditions.append("AD_SET_ID = %(ad_set_id)s")
            params["ad_set_id"] = ad_set_id

        # Build filter clause
        filter_clause = ""
        if conditions:
            filter_clause = "AND " + " AND ".join(conditions)

        query = f"""
            SELECT
                AD_SET_ID,
                AD_SET_NAME,
                CAMPAIGN_NAME,
                SUM(SPEND) AS TOTAL_SPEND,
                SUM(REACH) AS TOTAL_REACH,
                SUM(CLICKS) AS TOTAL_CLICKS,
                CASE WHEN SUM(IMPRESSIONS) > 0 THEN (SUM(CLICKS) / SUM(IMPRESSIONS)) * 100 ELSE 0 END AS CTR,
                CASE WHEN SUM(CLICKS) > 0 THEN SUM(SPEND) / SUM(CLICKS) ELSE 0 END AS CPC,
                SUM(IMPRESSIONS) AS TOTAL_IMPRESSIONS
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_AD_SET_PERFORMANCE
            WHERE PLATFORM = 'meta'
                {filter_clause}
            GROUP BY AD_SET_ID, AD_SET_NAME, CAMPAIGN_NAME
            ORDER BY TOTAL_SPEND DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
meta_ads_ad_set_repository = MetaAdsAdSetRepository()

"""
Meta Ads Ad Creatives repository - Data access layer for ad creative metrics.
"""
from datetime import date
from typing import Optional, List
from app.core.database import execute_query


class MetaAdsCreativeRepository:
    """Repository for Meta Ads creative data access operations."""

    @staticmethod
    def get_creatives(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        ad_id: Optional[str] = None
    ) -> List[dict]:
        """
        Fetch Meta Ads creative metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            ad_id: Optional ad ID filter

        Returns:
            List of dictionaries with creative metrics
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

        if ad_id:
            conditions.append("AD_ID = %(ad_id)s")
            params["ad_id"] = ad_id

        # Build filter clause
        filter_clause = ""
        if conditions:
            filter_clause = "AND " + " AND ".join(conditions)

        query = f"""
            SELECT
                AD_ID,
                MAX(AD_NAME) AS AD_NAME,
                MAX(AD_TYPE) AS AD_TYPE,
                SUM(SPEND) AS TOTAL_SPEND,
                SUM(IMPRESSIONS) AS TOTAL_IMPRESSIONS,
                SUM(CLICKS) AS TOTAL_CLICKS,
                COALESCE(SUM(CONVERSIONS), 0) AS TOTAL_CONVERSIONS,
                CASE WHEN SUM(IMPRESSIONS) > 0 THEN (SUM(CLICKS) / SUM(IMPRESSIONS)) * 100 ELSE 0 END AS CTR,
                CASE WHEN SUM(CLICKS) > 0 THEN SUM(SPEND) / SUM(CLICKS) ELSE 0 END AS CPC
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_AD_PERFORMANCE
            WHERE PLATFORM = 'meta'
                {filter_clause}
            GROUP BY AD_ID
            ORDER BY TOTAL_SPEND DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
meta_ads_creative_repository = MetaAdsCreativeRepository()

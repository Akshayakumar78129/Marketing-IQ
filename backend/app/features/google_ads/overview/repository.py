"""
Google Ads Overview repository - Data access layer for overview metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class GoogleAdsOverviewRepository:
    """Repository for Google Ads overview data access operations."""

    @staticmethod
    def get_overview_metrics(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> Optional[dict]:
        """
        Fetch aggregated Google Ads overview metrics, optionally filtered by date range.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            Dictionary with aggregated metrics or None if no data
        """
        # Build date filter conditions
        date_conditions = []
        params = {}

        if date_from:
            date_conditions.append("f.DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            date_conditions.append("f.DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        # Build the date filter clause
        date_filter = ""
        if date_conditions:
            date_filter = "AND " + " AND ".join(date_conditions)

        query = f"""
            SELECT
                perf.TOTAL_SPEND,
                perf.TOTAL_CONVERSIONS,
                perf.TOTAL_REVENUE,
                perf.ROAS,
                perf.CTR,
                perf.CPC,
                qs.AVG_QUALITY_SCORE
            FROM (
                SELECT
                    SUM(f.SPEND) AS TOTAL_SPEND,
                    SUM(f.CONVERSIONS) AS TOTAL_CONVERSIONS,
                    SUM(f.CONVERSION_VALUE) AS TOTAL_REVENUE,
                    CASE WHEN SUM(f.SPEND) > 0 THEN SUM(f.CONVERSION_VALUE) / SUM(f.SPEND) ELSE 0 END AS ROAS,
                    CASE WHEN SUM(f.IMPRESSIONS) > 0 THEN (SUM(f.CLICKS) / SUM(f.IMPRESSIONS)) * 100 ELSE 0 END AS CTR,
                    CASE WHEN SUM(f.CLICKS) > 0 THEN SUM(f.SPEND) / SUM(f.CLICKS) ELSE 0 END AS CPC
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE f
                JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_PLATFORM p ON f.PLATFORM = p.PLATFORM_CODE
                WHERE p.PLATFORM_CODE = 'google_ads'
                    {date_filter}
            ) perf
            CROSS JOIN (
                SELECT AVG(k.QUALITY_SCORE) AS AVG_QUALITY_SCORE
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_KEYWORD k
                JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_PLATFORM p ON k.PLATFORM = p.PLATFORM_CODE
                WHERE p.PLATFORM_CODE = 'google_ads'
                    AND k.QUALITY_SCORE IS NOT NULL
                    AND k.IS_CURRENT = TRUE
            ) qs
        """

        results = execute_query(query, params if params else None)
        return results[0] if results else None


# Singleton instance for dependency injection
google_ads_overview_repository = GoogleAdsOverviewRepository()

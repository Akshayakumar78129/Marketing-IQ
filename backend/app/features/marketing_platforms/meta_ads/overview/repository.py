"""
Meta Ads Overview repository - Data access layer for overview metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class MetaAdsOverviewRepository:
    """Repository for Meta Ads overview data access operations."""

    @staticmethod
    def get_overview_metrics(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> Optional[dict]:
        """
        Fetch aggregated Meta Ads overview metrics, optionally filtered by date range.

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

        # Build the date filter clause for performance table
        perf_date_filter = ""
        if date_conditions:
            perf_date_filter = "AND " + " AND ".join(date_conditions)

        # Build date filter for delivery table (uses 'd' alias)
        delivery_date_conditions = []
        if date_from:
            delivery_date_conditions.append("d.DATE_DAY >= %(date_from)s")
        if date_to:
            delivery_date_conditions.append("d.DATE_DAY <= %(date_to)s")

        delivery_date_filter = ""
        if delivery_date_conditions:
            delivery_date_filter = "AND " + " AND ".join(delivery_date_conditions)

        query = f"""
            SELECT
                perf.TOTAL_SPEND,
                perf.TOTAL_IMPRESSIONS,
                perf.TOTAL_CLICKS,
                COALESCE(perf.TOTAL_CONVERSIONS, 0) AS TOTAL_CONVERSIONS,
                COALESCE(perf.ROAS, 0) AS ROAS,
                perf.CTR,
                perf.CPC,
                perf.CPM,
                reach_data.TOTAL_REACH
            FROM (
                SELECT
                    SUM(f.SPEND) AS TOTAL_SPEND,
                    SUM(f.IMPRESSIONS) AS TOTAL_IMPRESSIONS,
                    SUM(f.CLICKS) AS TOTAL_CLICKS,
                    SUM(f.CONVERSIONS) AS TOTAL_CONVERSIONS,
                    CASE WHEN SUM(f.SPEND) > 0 THEN SUM(f.CONVERSION_VALUE) / SUM(f.SPEND) ELSE 0 END AS ROAS,
                    CASE WHEN SUM(f.IMPRESSIONS) > 0 THEN (SUM(f.CLICKS) / SUM(f.IMPRESSIONS)) * 100 ELSE 0 END AS CTR,
                    CASE WHEN SUM(f.CLICKS) > 0 THEN SUM(f.SPEND) / SUM(f.CLICKS) ELSE 0 END AS CPC,
                    CASE WHEN SUM(f.IMPRESSIONS) > 0 THEN (SUM(f.SPEND) / SUM(f.IMPRESSIONS)) * 1000 ELSE 0 END AS CPM
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE f
                WHERE f.PLATFORM = 'meta'
                    {perf_date_filter}
            ) perf
            CROSS JOIN (
                SELECT COALESCE(SUM(d.REACH), 0) AS TOTAL_REACH
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_META_DELIVERY d
                WHERE d.PLATFORM = 'meta'
                    {delivery_date_filter}
            ) reach_data
        """

        results = execute_query(query, params if params else None)
        return results[0] if results else None


# Singleton instance for dependency injection
meta_ads_overview_repository = MetaAdsOverviewRepository()

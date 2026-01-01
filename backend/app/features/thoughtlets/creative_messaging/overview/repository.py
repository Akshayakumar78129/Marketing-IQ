"""
Creative & Messaging - Overview repository - Data access layer.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class OverviewRepository:
    """Repository for creative messaging overview data access operations."""

    @staticmethod
    def get_overview_metrics(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> dict:
        """
        Fetch overview KPI metrics for creatives with performance data.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            Dictionary with overview metrics
        """
        date_conditions = []
        params = {}

        if date_from:
            date_conditions.append("p.date_day >= %(date_from)s::DATE")
            params["date_from"] = date_from.isoformat()

        if date_to:
            date_conditions.append("p.date_day <= %(date_to)s::DATE")
            params["date_to"] = date_to.isoformat()

        date_filter_ad = ""
        date_filter_campaign = ""
        if date_conditions:
            date_filter_ad = "AND " + " AND ".join(date_conditions)
            # For campaign performance, use cp alias
            date_filter_campaign = "AND " + " AND ".join(
                [c.replace("p.date_day", "cp.date_day") for c in date_conditions]
            )

        query = f"""
            WITH creative_metrics AS (
                SELECT
                    COUNT(DISTINCT c.creative_id) AS TOTAL_CREATIVES,
                    COUNT(DISTINCT CASE WHEN c.has_video = FALSE THEN c.creative_id END) AS IMAGE_CREATIVES,
                    COUNT(DISTINCT CASE WHEN c.has_video = TRUE THEN c.creative_id END) AS VIDEO_CREATIVES,
                    AVG(p.ctr) AS AVG_CTR,
                    AVG(p.cpc) AS AVG_CPC,
                    AVG(p.cpm) AS CPM
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_CREATIVE c
                JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_AD a ON c.creative_id = a.creative_id
                JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_AD_PERFORMANCE p ON a.ad_id = p.ad_id
                WHERE a.platform = 'meta'
                {date_filter_ad}
            ),
            campaign_metrics AS (
                SELECT
                    CASE WHEN SUM(cp.clicks) > 0 THEN SUM(cp.conversions) / SUM(cp.clicks) ELSE NULL END AS AVG_CVR,
                    CASE WHEN SUM(cp.spend) > 0 THEN SUM(cp.conversion_value) / SUM(cp.spend) ELSE NULL END AS OVERALL_ROAS
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE cp
                WHERE cp.platform = 'meta'
                {date_filter_campaign}
            )
            SELECT
                cm.TOTAL_CREATIVES,
                cm.IMAGE_CREATIVES,
                cm.VIDEO_CREATIVES,
                cm.AVG_CTR,
                camp.AVG_CVR,
                cm.AVG_CPC,
                cm.CPM,
                camp.OVERALL_ROAS
            FROM creative_metrics cm, campaign_metrics camp
        """

        results = execute_query(query, params if params else None)
        return results[0] if results else {}


# Singleton instance for dependency injection
overview_repository = OverviewRepository()

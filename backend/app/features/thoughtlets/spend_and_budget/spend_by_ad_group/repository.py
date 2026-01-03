"""
Thoughtlets Spend and Budget - Spend by Ad Group repository - Data access layer.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class SpendByAdGroupRepository:
    """Repository for spend by ad group data access operations."""

    @staticmethod
    def get_spend_by_ad_group(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch spend by ad group with optional date filters.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of ad group spend data
        """
        conditions = ["f.PLATFORM = 'google_ads'"]
        params = {}

        if date_from:
            conditions.append("f.DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            conditions.append("f.DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        where_clause = " AND ".join(conditions)

        query = f"""
            SELECT
                c.CAMPAIGN_NAME AS CAMPAIGN,
                SUM(f.IMPRESSIONS) AS IMPRESSIONS,
                SUM(f.CLICKS) AS CLICKS,
                SUM(f.SPEND) AS SPEND,
                SUM(f.CONVERSIONS) AS CONVERSIONS,
                SUM(f.CONVERSION_VALUE) / NULLIF(SUM(f.SPEND), 0) AS ROAS
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_AD_GROUP_PERFORMANCE f
            JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_AD_GROUP ag
                ON f.AD_GROUP_ID = ag.AD_GROUP_ID
                AND f.PLATFORM = ag.PLATFORM
                AND ag.IS_CURRENT = TRUE
            JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_CAMPAIGN c
                ON f.CAMPAIGN_ID = c.CAMPAIGN_ID
                AND f.PLATFORM = c.PLATFORM
                AND c.IS_CURRENT = TRUE
            WHERE {where_clause}
            GROUP BY c.CAMPAIGN_NAME
            ORDER BY SPEND DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
spend_by_ad_group_repository = SpendByAdGroupRepository()

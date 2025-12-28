"""
Meta Ads Demographics Age repository - Data access layer for age demographic metrics.
"""
from datetime import date
from typing import Optional, List
from app.core.database import execute_query


class MetaAdsDemographicsAgeRepository:
    """Repository for Meta Ads age demographics data access operations."""

    @staticmethod
    def get_demographics_age(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        age_bracket: Optional[str] = None
    ) -> List[dict]:
        """
        Fetch Meta Ads age demographic metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            age_bracket: Optional age bracket filter

        Returns:
            List of dictionaries with age demographic metrics
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

        if age_bracket:
            conditions.append("AGE_BRACKET = %(age_bracket)s")
            params["age_bracket"] = age_bracket

        # Build filter clause
        filter_clause = ""
        if conditions:
            filter_clause = "AND " + " AND ".join(conditions)

        query = f"""
            SELECT
                AGE_BRACKET,
                SUM(IMPRESSIONS) AS TOTAL_IMPRESSIONS,
                SUM(SPEND) AS TOTAL_SPEND,
                SUM(CLICKS) AS TOTAL_CLICKS,
                SUM(REACH) AS TOTAL_REACH,
                CASE WHEN SUM(IMPRESSIONS) > 0 THEN (SUM(CLICKS) / SUM(IMPRESSIONS)) * 100 ELSE 0 END AS CTR,
                CASE WHEN SUM(CLICKS) > 0 THEN SUM(SPEND) / SUM(CLICKS) ELSE 0 END AS CPC
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_META_DEMOGRAPHICS
            WHERE PLATFORM = 'meta'
                AND AGE_BRACKET IS NOT NULL
                {filter_clause}
            GROUP BY AGE_BRACKET
            ORDER BY TOTAL_SPEND DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
meta_ads_demographics_age_repository = MetaAdsDemographicsAgeRepository()

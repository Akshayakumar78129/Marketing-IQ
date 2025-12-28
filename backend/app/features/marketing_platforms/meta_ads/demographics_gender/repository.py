"""
Meta Ads Demographics Gender repository - Data access layer for gender demographic metrics.
"""
from datetime import date
from typing import Optional, List
from app.core.database import execute_query


class MetaAdsDemographicsGenderRepository:
    """Repository for Meta Ads gender demographics data access operations."""

    @staticmethod
    def get_demographics_gender(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        gender: Optional[str] = None
    ) -> List[dict]:
        """
        Fetch Meta Ads gender demographic metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            gender: Optional gender filter

        Returns:
            List of dictionaries with gender demographic metrics
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

        if gender:
            conditions.append("GENDER = %(gender)s")
            params["gender"] = gender.lower()

        # Build filter clause
        filter_clause = ""
        if conditions:
            filter_clause = "AND " + " AND ".join(conditions)

        query = f"""
            SELECT
                GENDER,
                SUM(IMPRESSIONS) AS TOTAL_IMPRESSIONS,
                SUM(SPEND) AS TOTAL_SPEND,
                SUM(CLICKS) AS TOTAL_CLICKS,
                SUM(REACH) AS TOTAL_REACH,
                CASE WHEN SUM(IMPRESSIONS) > 0 THEN (SUM(CLICKS) / SUM(IMPRESSIONS)) * 100 ELSE 0 END AS CTR,
                CASE WHEN SUM(CLICKS) > 0 THEN SUM(SPEND) / SUM(CLICKS) ELSE 0 END AS CPC
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_META_DEMOGRAPHICS
            WHERE PLATFORM = 'meta'
                AND GENDER IS NOT NULL
                {filter_clause}
            GROUP BY GENDER
            ORDER BY TOTAL_SPEND DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
meta_ads_demographics_gender_repository = MetaAdsDemographicsGenderRepository()

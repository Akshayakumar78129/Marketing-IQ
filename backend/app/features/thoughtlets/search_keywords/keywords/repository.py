"""
Search & Keywords - Keywords Performance repository - Data access layer.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class KeywordsRepository:
    """Repository for keywords performance data access operations."""

    @staticmethod
    def get_keywords_performance(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        match_type: Optional[str] = None,
        limit: int = 50
    ) -> list[dict]:
        """
        Fetch all keywords with performance metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            match_type: Optional filter by match type (EXACT, PHRASE, BROAD)
            limit: Number of results to return

        Returns:
            List of dictionaries with keyword performance data
        """
        conditions = []
        params = {"limit": limit}

        if date_from:
            conditions.append("f.DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            conditions.append("f.DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        if match_type:
            conditions.append("k.MATCH_TYPE = %(match_type)s")
            params["match_type"] = match_type.upper()

        filter_clause = ""
        if conditions:
            filter_clause = "AND " + " AND ".join(conditions)

        query = f"""
            SELECT
                k.KEYWORD_TEXT AS KEYWORD,
                k.MATCH_TYPE AS MATCH,
                SUM(f.IMPRESSIONS) AS IMPRESSIONS,
                SUM(f.CLICKS) AS CLICKS,
                ROUND(SUM(f.CLICKS) * 100.0 / NULLIF(SUM(f.IMPRESSIONS), 0), 1) AS CTR,
                ROUND(SUM(f.SPEND) / NULLIF(SUM(f.CLICKS), 0), 2) AS CPC,
                SUM(f.SPEND) AS SPEND,
                SUM(f.CONVERSIONS) AS CONVERSIONS,
                ROUND(SUM(f.CONVERSIONS) * 100.0 / NULLIF(SUM(f.CLICKS), 0), 2) AS CONV_RATE
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_KEYWORD_PERFORMANCE f
            JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_KEYWORD k
                ON f.KEYWORD_ID = k.KEYWORD_ID AND k.IS_CURRENT = TRUE
            WHERE f.PLATFORM = 'google_ads'
                {filter_clause}
            GROUP BY k.KEYWORD_TEXT, k.MATCH_TYPE
            ORDER BY IMPRESSIONS DESC
            LIMIT %(limit)s
        """

        results = execute_query(query, params)
        return results if results else []


# Singleton instance for dependency injection
keywords_repository = KeywordsRepository()

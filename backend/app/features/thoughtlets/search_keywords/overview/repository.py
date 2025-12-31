"""
Search & Keywords Overview repository - Data access layer for keyword metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class SearchKeywordsOverviewRepository:
    """Repository for search keywords overview data access operations."""

    @staticmethod
    def get_overview(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> dict:
        """
        Fetch aggregated keyword performance metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            Dictionary with aggregated keyword metrics
        """
        date_conditions = []
        params = {}

        if date_from:
            date_conditions.append("f.DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            date_conditions.append("f.DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        date_filter = ""
        if date_conditions:
            date_filter = "AND " + " AND ".join(date_conditions)

        query = f"""
            SELECT
                COUNT(DISTINCT f.KEYWORD_ID) AS TOTAL_KEYWORDS,
                COUNT(DISTINCT CASE WHEN k.MATCH_TYPE = 'EXACT' THEN k.KEYWORD_ID END) AS EXACT_MATCH,
                COUNT(DISTINCT CASE WHEN k.MATCH_TYPE = 'PHRASE' THEN k.KEYWORD_ID END) AS PHRASE_MATCH,
                COUNT(DISTINCT CASE WHEN k.MATCH_TYPE = 'BROAD' THEN k.KEYWORD_ID END) AS BROAD_MATCH,
                ROUND(SUM(f.CLICKS) * 100.0 / NULLIF(SUM(f.IMPRESSIONS), 0), 1) AS AVG_CTR,
                ROUND(SUM(f.SPEND) / NULLIF(SUM(f.CLICKS), 0), 2) AS AVG_CPC,
                SUM(f.CONVERSIONS) AS CONVERSIONS,
                SUM(f.SPEND) AS TOTAL_SPEND
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_KEYWORD_PERFORMANCE f
            JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_KEYWORD k
                ON f.KEYWORD_ID = k.KEYWORD_ID AND k.IS_CURRENT = TRUE
            WHERE f.PLATFORM = 'google_ads'
                {date_filter}
        """

        results = execute_query(query, params if params else None)
        return results[0] if results else {}


# Singleton instance for dependency injection
search_keywords_overview_repository = SearchKeywordsOverviewRepository()

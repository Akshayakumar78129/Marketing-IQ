"""
Google Ads Keyword Performance repository - Data access layer for keyword performance metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class KeywordPerformanceRepository:
    """Repository for Google Ads keyword performance data access operations."""

    @staticmethod
    def get_keyword_performance(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch Google Ads keyword performance metrics with optional date filters.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            List of dictionaries with keyword performance metrics
        """
        # Build filter conditions
        conditions = []
        params = {}

        if date_from:
            conditions.append("f.DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            conditions.append("f.DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        # Build the filter clause
        filter_clause = ""
        if conditions:
            filter_clause = "AND " + " AND ".join(conditions)

        query = f"""
            SELECT
                k.KEYWORD_TEXT AS "KEYWORD",
                k.MATCH_TYPE AS "MATCH",
                SUM(f.IMPRESSIONS) AS "IMPRESSIONS",
                SUM(f.CLICKS) AS "CLICKS",
                ROUND(SUM(f.CLICKS) * 100.0 / NULLIF(SUM(f.IMPRESSIONS), 0), 1) AS "CTR",
                ROUND(SUM(f.SPEND) / NULLIF(SUM(f.CLICKS), 0), 0) AS "CPC",
                ROUND(SUM(f.CONVERSIONS), 0) AS "CONVERSIONS",
                ROUND(SUM(f.SPEND), 0) AS "COST"
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_KEYWORD_PERFORMANCE f
            JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_KEYWORD k
                ON f.KEYWORD_ID = k.KEYWORD_ID
                AND f.PLATFORM = k.PLATFORM
                AND k.IS_CURRENT = TRUE
            WHERE f.PLATFORM = 'google_ads'
                {filter_clause}
            GROUP BY k.KEYWORD_TEXT, k.MATCH_TYPE
            ORDER BY "IMPRESSIONS" DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
keyword_performance_repository = KeywordPerformanceRepository()

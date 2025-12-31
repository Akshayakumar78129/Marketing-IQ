"""
Search & Keywords Top Keywords repository - Data access layer for top keywords.
"""
from datetime import date
from typing import Optional, Literal
from app.core.database import execute_query


class TopKeywordsRepository:
    """Repository for top keywords data access operations."""

    @staticmethod
    def get_top_keywords(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        sort_by: Literal["conversions", "clicks"] = "conversions",
        limit: int = 10
    ) -> list[dict]:
        """
        Fetch top keywords by conversions or clicks.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            sort_by: Sort by 'conversions' or 'clicks'
            limit: Number of results to return

        Returns:
            List of dictionaries with top keyword data
        """
        date_conditions = []
        params = {"limit": limit}

        if date_from:
            date_conditions.append("f.DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            date_conditions.append("f.DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        date_filter = ""
        if date_conditions:
            date_filter = "AND " + " AND ".join(date_conditions)

        # Determine sort column
        sort_column = "CONVERSIONS" if sort_by == "conversions" else "CLICKS"

        query = f"""
            SELECT
                k.KEYWORD_TEXT AS KEYWORD,
                SUM(f.CONVERSIONS) AS CONVERSIONS,
                SUM(f.CLICKS) AS CLICKS
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_KEYWORD_PERFORMANCE f
            JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_KEYWORD k
                ON f.KEYWORD_ID = k.KEYWORD_ID AND k.IS_CURRENT = TRUE
            WHERE f.PLATFORM = 'google_ads'
                {date_filter}
            GROUP BY k.KEYWORD_TEXT
            ORDER BY {sort_column} DESC
            LIMIT %(limit)s
        """

        results = execute_query(query, params)
        return results if results else []


# Singleton instance for dependency injection
top_keywords_repository = TopKeywordsRepository()

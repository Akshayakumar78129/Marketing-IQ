"""
Google Ads Account Health repository - Data access layer for account health metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class AccountHealthRepository:
    """Repository for Google Ads account health data access operations."""

    @staticmethod
    def get_account_health(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> dict:
        """
        Fetch Google Ads account health metrics with optional date filters.

        Args:
            date_from: Optional start date for metrics
            date_to: Optional end date for metrics

        Returns:
            Dictionary with account health metrics
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

        # Build the filter clause
        date_filter = ""
        if conditions:
            date_filter = "AND " + " AND ".join(conditions)

        query = f"""
            SELECT
                (SELECT COUNT(DISTINCT CAMPAIGN_ID)
                 FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE
                 WHERE PLATFORM = 'google_ads'
                   {date_filter}) AS "TOTAL_CAMPAIGNS",

                (SELECT COUNT(DISTINCT f.CAMPAIGN_ID)
                 FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE f
                 JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_CAMPAIGN c
                   ON f.CAMPAIGN_ID = c.CAMPAIGN_ID AND f.PLATFORM = c.PLATFORM AND c.IS_CURRENT = TRUE
                 WHERE f.PLATFORM = 'google_ads'
                   AND c.STATUS = 'ENABLED'
                   {date_filter.replace('DATE_DAY', 'f.DATE_DAY')}) AS "ACTIVE_CAMPAIGNS",

                (SELECT ROUND(SUM(CONVERSION_VALUE) / NULLIF(SUM(SPEND), 0), 2)
                 FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE
                 WHERE PLATFORM = 'google_ads'
                   {date_filter}) AS "AVG_ROAS",

                (SELECT COUNT(DISTINCT KEYWORD_ID)
                 FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_KEYWORD_PERFORMANCE
                 WHERE PLATFORM = 'google_ads'
                   {date_filter}) AS "TOTAL_KEYWORDS"
        """

        results = execute_query(query, params if params else None)
        return results[0] if results else {}


# Singleton instance for dependency injection
account_health_repository = AccountHealthRepository()

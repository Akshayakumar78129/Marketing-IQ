"""
Audience & Behavioral Overview repository - Data access layer for audience/behavioral metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class AudienceBehavioralOverviewRepository:
    """Repository for audience and behavioral overview data access operations."""

    @staticmethod
    def get_overview(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> dict:
        """
        Fetch aggregated audience and behavioral metrics from GA4 data.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            Dictionary with aggregated audience and behavioral metrics
        """
        date_conditions = []
        params = {}

        if date_from:
            date_conditions.append("DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            date_conditions.append("DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        date_filter = ""
        if date_conditions:
            date_filter = "AND " + " AND ".join(date_conditions)

        query = f"""
            SELECT
                sessions.TOTAL_USERS,
                sessions.TOTAL_SESSIONS,
                events.NEW_USERS,
                GREATEST(sessions.TOTAL_USERS - events.NEW_USERS, 0) AS RETURNING_USERS,
                sessions.ENGAGEMENT_RATE,
                sessions.BOUNCE_RATE,
                sessions.SESSIONS_PER_USER,
                sessions.CONVERSION_RATE
            FROM (
                SELECT
                    SUM(TOTAL_USERS) AS TOTAL_USERS,
                    SUM(TOTAL_SESSIONS) AS TOTAL_SESSIONS,
                    ROUND(AVG(ENGAGEMENT_RATE_PCT), 1) AS ENGAGEMENT_RATE,
                    ROUND(AVG(BOUNCE_PROXY_PCT), 1) AS BOUNCE_RATE,
                    ROUND(SUM(TOTAL_SESSIONS) * 1.0 / NULLIF(SUM(TOTAL_USERS), 0), 3) AS SESSIONS_PER_USER,
                    ROUND(SUM(TOTAL_KEY_EVENTS) * 100.0 / NULLIF(SUM(TOTAL_SESSIONS), 0), 1) AS CONVERSION_RATE
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_SESSIONS
                WHERE PLATFORM = 'ga4'
                    {date_filter}
            ) sessions
            CROSS JOIN (
                SELECT
                    COALESCE(SUM(EVENT_COUNT), 0) AS NEW_USERS
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_EVENTS
                WHERE PLATFORM = 'ga4'
                    AND EVENT_NAME = 'first_visit'
                    {date_filter}
            ) events
        """

        results = execute_query(query, params if params else None)
        return results[0] if results else {}


# Singleton instance for dependency injection
audience_behavioral_overview_repository = AudienceBehavioralOverviewRepository()

"""
Engagement Funnel repository - Data access layer for engagement funnel metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class EngagementFunnelRepository:
    """Repository for engagement funnel data access operations."""

    @staticmethod
    def get_engagement_funnel(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> dict:
        """
        Fetch engagement funnel metrics (users, sessions, engaged, conversions).

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            Dictionary with engagement funnel metrics
        """
        date_conditions_sessions = []
        date_conditions_conversions = []
        params = {}

        if date_from:
            date_conditions_sessions.append("s.DATE_DAY >= %(date_from)s")
            date_conditions_conversions.append("c.DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            date_conditions_sessions.append("s.DATE_DAY <= %(date_to)s")
            date_conditions_conversions.append("c.DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        sessions_filter = ""
        if date_conditions_sessions:
            sessions_filter = "WHERE " + " AND ".join(date_conditions_sessions)

        conversions_filter = ""
        if date_conditions_conversions:
            conversions_filter = "WHERE " + " AND ".join(date_conditions_conversions)

        query = f"""
            SELECT
                sessions.TOTAL_USERS,
                sessions.TOTAL_SESSIONS,
                sessions.ENGAGED_SESSIONS,
                COALESCE(conversions.TOTAL_CONVERSIONS, 0) AS TOTAL_CONVERSIONS
            FROM (
                SELECT
                    SUM(s.TOTAL_USERS) AS TOTAL_USERS,
                    SUM(s.TOTAL_SESSIONS) AS TOTAL_SESSIONS,
                    SUM(s.ENGAGED_SESSIONS) AS ENGAGED_SESSIONS
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_SESSIONS s
                {sessions_filter}
            ) sessions
            CROSS JOIN (
                SELECT
                    SUM(c.CONVERSIONS) AS TOTAL_CONVERSIONS
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_CONVERSIONS c
                {conversions_filter}
            ) conversions
        """

        results = execute_query(query, params if params else None)
        return results[0] if results else {}


# Singleton instance for dependency injection
engagement_funnel_repository = EngagementFunnelRepository()

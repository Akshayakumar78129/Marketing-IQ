"""
GA4 Analytics Conversion Funnel repository - Data access layer for conversion funnel metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class GA4ConversionFunnelRepository:
    """Repository for GA4 Analytics conversion funnel data access operations."""

    @staticmethod
    def get_conversion_funnel(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> Optional[dict]:
        """
        Fetch conversion funnel metrics (sessions, product views, add to cart, purchases).

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            Dictionary with conversion funnel metrics or None if no data
        """
        # Build date filter conditions
        date_conditions_sessions = []
        date_conditions_ecom = []
        params = {}

        if date_from:
            date_conditions_sessions.append("DATE_DAY >= %(date_from)s")
            date_conditions_ecom.append("DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            date_conditions_sessions.append("DATE_DAY <= %(date_to)s")
            date_conditions_ecom.append("DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        # Build the date filter clauses
        sessions_date_filter = ""
        if date_conditions_sessions:
            sessions_date_filter = "AND " + " AND ".join(date_conditions_sessions)

        ecom_date_filter = ""
        if date_conditions_ecom:
            ecom_date_filter = "AND " + " AND ".join(date_conditions_ecom)

        query = f"""
            SELECT
                sessions.SESSIONS,
                ecom.PRODUCT_VIEWS,
                ecom.ADD_TO_CART,
                ecom.PURCHASES
            FROM (
                SELECT SUM(TOTAL_SESSIONS) AS SESSIONS
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_SESSIONS
                WHERE PLATFORM = 'ga4'
                    {sessions_date_filter}
            ) sessions
            CROSS JOIN (
                SELECT
                    SUM(ITEMS_VIEWED) AS PRODUCT_VIEWS,
                    SUM(ITEMS_ADDED_TO_CART) AS ADD_TO_CART,
                    SUM(ITEMS_PURCHASED) AS PURCHASES
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_ECOMMERCE_ITEM
                WHERE PLATFORM = 'ga4'
                    {ecom_date_filter}
            ) ecom
        """

        results = execute_query(query, params if params else None)
        return results[0] if results else None


# Singleton instance for dependency injection
ga4_conversion_funnel_repository = GA4ConversionFunnelRepository()

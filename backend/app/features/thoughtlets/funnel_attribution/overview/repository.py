"""
Funnel & Attribution Overview repository - Data access layer for funnel/attribution metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class FunnelAttributionOverviewRepository:
    """Repository for funnel and attribution overview data access operations."""

    @staticmethod
    def get_overview(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> dict:
        """
        Fetch aggregated funnel and attribution metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            Dictionary with aggregated funnel and attribution metrics
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
            date_filter = "WHERE " + " AND ".join(date_conditions)

        # Build order date filter for FCT_MAGENTO_ORDER
        order_date_conditions = []
        if date_from:
            order_date_conditions.append("ORDER_DATE_DAY >= %(date_from)s")
        if date_to:
            order_date_conditions.append("ORDER_DATE_DAY <= %(date_to)s")

        order_date_filter = ""
        if order_date_conditions:
            order_date_filter = "WHERE " + " AND ".join(order_date_conditions) + " AND STATUS NOT IN ('canceled', 'fraud')"
        else:
            order_date_filter = "WHERE STATUS NOT IN ('canceled', 'fraud')"

        query = f"""
            WITH session_metrics AS (
                SELECT
                    SUM(TOTAL_SESSIONS) AS TOTAL_SESSIONS,
                    SUM(ENGAGED_SESSIONS) AS ENGAGED_SESSIONS,
                    ROUND(SUM(ENGAGED_SESSIONS) * 100.0 / NULLIF(SUM(TOTAL_SESSIONS), 0), 1) AS ENGAGEMENT_RATE
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_SESSIONS
                {date_filter}
            ),
            ecommerce_metrics AS (
                SELECT
                    SUM(ITEMS_VIEWED) AS ITEMS_VIEWED,
                    SUM(ITEMS_ADDED_TO_CART) AS ITEMS_ADDED_TO_CART,
                    SUM(ITEMS_PURCHASED) AS ITEMS_PURCHASED,
                    ROUND(SUM(ITEMS_ADDED_TO_CART) * 100.0 / NULLIF(SUM(ITEMS_VIEWED), 0), 1) AS VIEW_TO_CART_PCT,
                    ROUND(SUM(ITEMS_PURCHASED) * 100.0 / NULLIF(SUM(ITEMS_ADDED_TO_CART), 0), 1) AS CART_TO_PURCHASE_PCT
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_ECOMMERCE_ITEM
                {date_filter}
            ),
            utm_metrics AS (
                SELECT
                    SUM(SESSIONS) AS TOTAL_SESSIONS,
                    SUM(CASE WHEN SOURCE NOT IN ('(direct)', '(not set)') AND MEDIUM NOT IN ('(none)', '(not set)') THEN SESSIONS ELSE 0 END) AS UTM_SESSIONS
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_TRAFFIC
                {date_filter}
            ),
            conversion_metrics AS (
                SELECT
                    COALESCE(SUM(CONVERSIONS), 0) AS TOTAL_CONVERSIONS
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_GA4_CONVERSIONS
                {date_filter}
            ),
            order_metrics AS (
                SELECT
                    COUNT(*) AS ORDER_COUNT,
                    COALESCE(AVG(GRAND_TOTAL), 0) AS AVG_ORDER_VALUE
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_MAGENTO_ORDER
                {order_date_filter}
            )
            SELECT
                s.TOTAL_SESSIONS,
                s.ENGAGEMENT_RATE,
                e.VIEW_TO_CART_PCT,
                COALESCE(e.CART_TO_PURCHASE_PCT, 0) AS CART_TO_PURCHASE_PCT,
                CASE WHEN e.ITEMS_ADDED_TO_CART > 0 AND e.ITEMS_PURCHASED = 0 THEN 100.0
                     WHEN e.ITEMS_ADDED_TO_CART > 0 THEN ROUND((1 - (e.ITEMS_PURCHASED * 1.0 / e.ITEMS_ADDED_TO_CART)) * 100, 1)
                     ELSE 0 END AS CART_ABANDON_RATE,
                c.TOTAL_CONVERSIONS,
                ROUND(u.UTM_SESSIONS * 100.0 / NULLIF(u.TOTAL_SESSIONS, 0), 1) AS UTM_COVERAGE_PCT,
                ROUND(o.AVG_ORDER_VALUE, 2) AS AVG_ORDER_VALUE
            FROM session_metrics s
            CROSS JOIN ecommerce_metrics e
            CROSS JOIN utm_metrics u
            CROSS JOIN conversion_metrics c
            CROSS JOIN order_metrics o
        """

        results = execute_query(query, params if params else None)
        return results[0] if results else {}


# Singleton instance for dependency injection
funnel_attribution_overview_repository = FunnelAttributionOverviewRepository()

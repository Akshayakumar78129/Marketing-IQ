"""
eCommerce Funnel repository - Data access layer for eCommerce funnel metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class EcommerceFunnelRepository:
    """Repository for eCommerce funnel data access operations."""

    @staticmethod
    def get_funnel_metrics(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> dict:
        """
        Fetch eCommerce funnel metrics (View → Cart → Purchase).

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            Dictionary with funnel metrics (views, add_to_cart, purchase)
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

        query = f"""
            SELECT
                SUM(ITEMS_VIEWED) AS VIEWS,
                SUM(ITEMS_ADDED_TO_CART) AS ADD_TO_CART,
                SUM(ITEMS_PURCHASED) AS PURCHASE
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_ECOMMERCE_ITEM
            {date_filter}
        """

        results = execute_query(query, params if params else None)
        return results[0] if results else {}


# Singleton instance for dependency injection
ecommerce_funnel_repository = EcommerceFunnelRepository()

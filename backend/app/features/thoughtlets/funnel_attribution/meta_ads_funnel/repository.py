"""
Meta Ads Funnel repository - Data access layer for Meta pixel conversion events.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class MetaAdsFunnelRepository:
    """Repository for Meta Ads funnel data access operations."""

    @staticmethod
    def get_funnel_metrics(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> dict:
        """
        Fetch Meta Ads funnel metrics (pixel conversion events).

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            Dictionary with funnel metrics (view_content, add_to_cart, initiate_checkout, purchase)
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
                ROUND(SUM(VIEW_CONTENT)) AS VIEW_CONTENT,
                ROUND(SUM(ADD_TO_CART)) AS ADD_TO_CART,
                ROUND(SUM(INITIATE_CHECKOUT)) AS INITIATE_CHECKOUT,
                ROUND(SUM(PURCHASES)) AS PURCHASE
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_META_CONVERSION
            {date_filter}
        """

        results = execute_query(query, params if params else None)
        return results[0] if results else {}


# Singleton instance for dependency injection
meta_ads_funnel_repository = MetaAdsFunnelRepository()

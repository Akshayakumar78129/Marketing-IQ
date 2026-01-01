"""
Creative & Messaging - CTA Types repository - Data access layer.
"""
from datetime import date
from typing import Optional, List
from app.core.database import execute_query


class CTATypesRepository:
    """Repository for CTA types data access operations."""

    @staticmethod
    def get_cta_types(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> List[dict]:
        """
        Fetch CTA type distribution for bar chart.

        Args:
            date_from: Optional start date for filtering
            date_to: Optional end date for filtering

        Returns:
            List of dictionaries with cta_type and count
        """
        date_conditions = []
        params = {}

        if date_from:
            date_conditions.append("p.date_day >= %(date_from)s::DATE")
            params["date_from"] = date_from.isoformat()

        if date_to:
            date_conditions.append("p.date_day <= %(date_to)s::DATE")
            params["date_to"] = date_to.isoformat()

        date_filter = ""
        if date_conditions:
            date_filter = "AND " + " AND ".join(date_conditions)

        query = f"""
            SELECT
                COALESCE(c.call_to_action_type, 'NO_BUTTON') AS CTA_TYPE,
                COUNT(DISTINCT c.creative_id) AS COUNT
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_CREATIVE c
            JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_AD a ON c.creative_id = a.creative_id
            JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_AD_PERFORMANCE p ON a.ad_id = p.ad_id
            WHERE a.platform = 'meta'
            {date_filter}
            GROUP BY c.call_to_action_type
            ORDER BY COUNT DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
cta_types_repository = CTATypesRepository()

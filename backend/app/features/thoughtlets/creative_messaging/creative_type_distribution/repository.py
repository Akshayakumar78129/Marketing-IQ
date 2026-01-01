"""
Creative & Messaging - Creative Type Distribution repository - Data access layer.
"""
from datetime import date
from typing import Optional, List
from app.core.database import execute_query


class CreativeTypeDistributionRepository:
    """Repository for creative type distribution data access operations."""

    @staticmethod
    def get_creative_type_distribution(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> List[dict]:
        """
        Fetch creative type distribution for pie chart.

        Args:
            date_from: Optional start date for filtering
            date_to: Optional end date for filtering

        Returns:
            List of dictionaries with creative_type and count
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
                COALESCE(c.creative_type, 'UNKNOWN') AS CREATIVE_TYPE,
                COUNT(DISTINCT c.creative_id) AS COUNT
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_CREATIVE c
            JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_AD a ON c.creative_id = a.creative_id
            JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_AD_PERFORMANCE p ON a.ad_id = p.ad_id
            WHERE a.platform = 'meta'
            {date_filter}
            GROUP BY 1
            ORDER BY COUNT DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
creative_type_distribution_repository = CreativeTypeDistributionRepository()

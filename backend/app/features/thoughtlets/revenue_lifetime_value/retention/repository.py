"""
Revenue & Lifetime Value - Retention repository - Data access layer.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class RetentionRepository:
    """Repository for retention data access operations."""

    @staticmethod
    def get_retention_metrics(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> dict:
        """
        Fetch retention metrics from FCT_CUSTOMER_METRICS.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            Dictionary with retention metrics
        """
        date_conditions = []
        params = {}

        if date_from:
            date_conditions.append("COHORT_MONTH >= DATE_TRUNC('MONTH', %(date_from)s::DATE)")
            params["date_from"] = date_from.isoformat()

        if date_to:
            date_conditions.append("COHORT_MONTH <= DATE_TRUNC('MONTH', %(date_to)s::DATE)")
            params["date_to"] = date_to.isoformat()

        date_filter = ""
        if date_conditions:
            date_filter = "WHERE " + " AND ".join(date_conditions)

        query = f"""
            SELECT
                AVG(RETENTION_RATE_30D) AS RETENTION_30D,
                AVG(RETENTION_RATE_60D) AS RETENTION_60D,
                AVG(RETENTION_RATE_90D) AS RETENTION_90D,
                SUM(RETAINED_30D_COUNT) AS RETAINED_30D_COUNT,
                SUM(RETAINED_60D_COUNT) AS RETAINED_60D_COUNT,
                SUM(RETAINED_90D_COUNT) AS RETAINED_90D_COUNT
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CUSTOMER_METRICS
            {date_filter}
        """

        results = execute_query(query, params if params else None)
        return results[0] if results else {}


# Singleton instance for dependency injection
retention_repository = RetentionRepository()

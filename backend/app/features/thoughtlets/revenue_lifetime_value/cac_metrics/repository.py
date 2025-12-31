"""
Revenue & Lifetime Value - CAC Metrics repository - Data access layer.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class CACMetricsRepository:
    """Repository for CAC metrics data access operations."""

    @staticmethod
    def get_cac_metrics(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> dict:
        """
        Fetch CAC metrics from FCT_CUSTOMER_METRICS.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            Dictionary with CAC metrics
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
                AVG(CAC_GOOGLE) AS CAC_GOOGLE,
                AVG(CAC_META) AS CAC_META,
                AVG(CAC) AS CAC_BLENDED,
                SUM(GOOGLE_ADS_SPEND) AS GOOGLE_ADS_SPEND,
                SUM(META_ADS_SPEND) AS META_ADS_SPEND,
                SUM(TOTAL_AD_SPEND) AS TOTAL_AD_SPEND
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CUSTOMER_METRICS
            {date_filter}
        """

        results = execute_query(query, params if params else None)
        return results[0] if results else {}


# Singleton instance for dependency injection
cac_metrics_repository = CACMetricsRepository()

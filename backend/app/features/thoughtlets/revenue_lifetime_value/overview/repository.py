"""
Revenue & Lifetime Value Overview repository - Data access layer for CLV metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class RevenueOverviewRepository:
    """Repository for revenue overview data access operations."""

    @staticmethod
    def get_metrics_data(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> dict:
        """
        Fetch aggregated metrics from FCT_CUSTOMER_METRICS.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            Dictionary with aggregated metrics
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
                SUM(TOTAL_REVENUE) AS TOTAL_REVENUE,
                AVG(REPEAT_PURCHASE_RATE) AS REPEAT_PURCHASE_RATE,
                AVG(LTV_CAC_RATIO) AS CLV_CAC_RATIO,
                SUM(TOTAL_REVENUE) / NULLIF(SUM(TOTAL_ORDERS), 0) AS AVG_AOV
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CUSTOMER_METRICS
            {date_filter}
        """

        results = execute_query(query, params if params else None)
        return results[0] if results else {}

    @staticmethod
    def get_clv_data() -> dict:
        """
        Fetch CLV averages and churn risk from DIM_PERSON.

        Returns:
            Dictionary with CLV metrics and churn risk percentage
        """
        query = """
            SELECT
                AVG(TOTAL_CLV) AS AVG_CLV,
                AVG(HISTORIC_CLV) AS HISTORIC_CLV,
                AVG(PREDICTED_CLV) AS PREDICTED_CLV,
                AVG(CHURN_PROBABILITY) * 100.0 AS CHURN_RISK
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_PERSON
        """

        results = execute_query(query)
        return results[0] if results else {}


# Singleton instance for dependency injection
revenue_overview_repository = RevenueOverviewRepository()

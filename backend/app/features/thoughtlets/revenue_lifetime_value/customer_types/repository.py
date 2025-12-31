"""
Revenue & Lifetime Value - Customer Types repository - Data access layer.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class CustomerTypesRepository:
    """Repository for customer types data access operations."""

    @staticmethod
    def get_customer_types(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> dict:
        """
        Fetch customer type counts from FCT_CUSTOMER_METRICS.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            Dictionary with customer type counts
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
                SUM(NEW_CUSTOMERS) AS NEW_CUSTOMERS,
                SUM(REPEAT_CUSTOMERS) AS REPEAT_CUSTOMERS,
                SUM(ONE_TIME_CUSTOMERS) AS ONE_TIME_CUSTOMERS
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CUSTOMER_METRICS
            {date_filter}
        """

        results = execute_query(query, params if params else None)
        return results[0] if results else {}


# Singleton instance for dependency injection
customer_types_repository = CustomerTypesRepository()

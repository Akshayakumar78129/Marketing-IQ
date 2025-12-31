"""
Revenue & Lifetime Value - Cohort Retention repository - Data access layer.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class CohortRetentionRepository:
    """Repository for cohort retention data access operations."""

    @staticmethod
    def get_cohort_retention(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 12
    ) -> list[dict]:
        """
        Fetch cohort retention data calculated from FCT_ORDER_DETAILS.

        Calculates monthly cohort retention by:
        1. Determining each customer's cohort (month of first order)
        2. Tracking which months they placed subsequent orders
        3. Calculating retention rate for each month since cohort start

        Args:
            date_from: Optional start date for filtering cohorts
            date_to: Optional end date for filtering cohorts
            limit: Number of cohorts to return (default: 12)

        Returns:
            List of dictionaries with cohort retention data
        """
        cohort_conditions = []
        params = {"limit": limit}

        if date_from:
            cohort_conditions.append("cohort_month >= DATE_TRUNC('MONTH', %(date_from)s::DATE)")
            params["date_from"] = date_from.isoformat()

        if date_to:
            cohort_conditions.append("cohort_month <= DATE_TRUNC('MONTH', %(date_to)s::DATE)")
            params["date_to"] = date_to.isoformat()

        cohort_filter = ""
        if cohort_conditions:
            cohort_filter = "WHERE " + " AND ".join(cohort_conditions)

        query = f"""
            WITH cohort_base AS (
                SELECT
                    PERSON_ID,
                    DATE_TRUNC('MONTH', MIN(ORDER_DATE)) AS cohort_month
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_ORDER_DETAILS
                GROUP BY PERSON_ID
            ),
            cohort_activity AS (
                SELECT
                    c.cohort_month,
                    DATEDIFF('MONTH', c.cohort_month, DATE_TRUNC('MONTH', o.ORDER_DATE)) AS months_since,
                    COUNT(DISTINCT c.PERSON_ID) AS active_customers
                FROM cohort_base c
                JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_ORDER_DETAILS o
                    ON c.PERSON_ID = o.PERSON_ID
                GROUP BY c.cohort_month, months_since
            ),
            cohort_initial AS (
                SELECT cohort_month, active_customers AS initial_size
                FROM cohort_activity
                WHERE months_since = 0
            ),
            filtered_cohorts AS (
                SELECT DISTINCT cohort_month
                FROM cohort_activity
                {cohort_filter}
            )
            SELECT
                ca.cohort_month AS COHORT_MONTH,
                ci.initial_size AS INITIAL_SIZE,
                ca.months_since AS MONTHS_SINCE,
                ca.active_customers AS ACTIVE_CUSTOMERS,
                ROUND(ca.active_customers * 100.0 / ci.initial_size, 2) AS RETENTION_RATE
            FROM cohort_activity ca
            JOIN cohort_initial ci ON ca.cohort_month = ci.cohort_month
            WHERE ca.cohort_month IN (SELECT cohort_month FROM filtered_cohorts)
            ORDER BY ca.cohort_month DESC, ca.months_since ASC
            LIMIT %(limit)s
        """

        results = execute_query(query, params)
        return results if results else []


# Singleton instance for dependency injection
cohort_retention_repository = CohortRetentionRepository()

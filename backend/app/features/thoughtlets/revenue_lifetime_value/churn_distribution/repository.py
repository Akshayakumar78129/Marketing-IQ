"""
Revenue & Lifetime Value - Churn Distribution repository - Data access layer.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class ChurnDistributionRepository:
    """Repository for churn distribution data access operations."""

    @staticmethod
    def get_churn_distribution(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch churn risk distribution from DIM_PERSON.

        Args:
            date_from: Optional start date (filter by ORDER_DATE via FCT_ORDER_DETAILS)
            date_to: Optional end date (filter by ORDER_DATE via FCT_ORDER_DETAILS)

        Returns:
            List of dictionaries with risk level and customer count
        """
        if date_from or date_to:
            # Filter by customers who had any order in the date range
            date_conditions = []
            params = {}

            if date_from:
                date_conditions.append("o.ORDER_DATE >= %(date_from)s")
                params["date_from"] = date_from.isoformat()

            if date_to:
                date_conditions.append("o.ORDER_DATE <= %(date_to)s")
                params["date_to"] = date_to.isoformat()

            date_filter = "WHERE " + " AND ".join(date_conditions)

            query = f"""
                SELECT
                    p.CHURN_RISK_SEGMENT AS RISK_LEVEL,
                    COUNT(DISTINCT p.PERSON_ID) AS CUSTOMER_COUNT
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_PERSON p
                JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_ORDER_DETAILS o
                    ON p.PERSON_ID = o.PERSON_ID
                {date_filter}
                GROUP BY p.CHURN_RISK_SEGMENT
                ORDER BY
                    CASE p.CHURN_RISK_SEGMENT
                        WHEN 'Low Risk' THEN 1
                        WHEN 'Healthy' THEN 2
                        WHEN 'Medium Risk' THEN 3
                        WHEN 'High Risk' THEN 4
                    END
            """

            results = execute_query(query, params)
        else:
            # No date filter - return all customers
            query = """
                SELECT
                    CHURN_RISK_SEGMENT AS RISK_LEVEL,
                    COUNT(*) AS CUSTOMER_COUNT
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_PERSON
                GROUP BY CHURN_RISK_SEGMENT
                ORDER BY
                    CASE CHURN_RISK_SEGMENT
                        WHEN 'Low Risk' THEN 1
                        WHEN 'Healthy' THEN 2
                        WHEN 'Medium Risk' THEN 3
                        WHEN 'High Risk' THEN 4
                    END
            """

            results = execute_query(query)

        return results if results else []


# Singleton instance for dependency injection
churn_distribution_repository = ChurnDistributionRepository()

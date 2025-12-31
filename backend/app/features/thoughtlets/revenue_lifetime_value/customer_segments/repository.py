"""
Revenue & Lifetime Value - Customer Segments repository - Data access layer.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class CustomerSegmentsRepository:
    """Repository for customer segments data access operations."""

    @staticmethod
    def get_customer_segments(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> list[dict]:
        """
        Fetch customer count by CLV segment from DIM_PERSON.

        Args:
            date_from: Optional start date (filter by ORDER_DATE via FCT_ORDER_DETAILS)
            date_to: Optional end date (filter by ORDER_DATE via FCT_ORDER_DETAILS)

        Returns:
            List of dictionaries with segment name and customer count
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
                    p.CLV_SEGMENT AS SEGMENT_NAME,
                    COUNT(DISTINCT p.PERSON_ID) AS CUSTOMER_COUNT
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_PERSON p
                JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_ORDER_DETAILS o
                    ON p.PERSON_ID = o.PERSON_ID
                {date_filter}
                GROUP BY p.CLV_SEGMENT
                ORDER BY CUSTOMER_COUNT DESC
            """

            results = execute_query(query, params)
        else:
            # No date filter - return all customers
            query = """
                SELECT
                    CLV_SEGMENT AS SEGMENT_NAME,
                    COUNT(*) AS CUSTOMER_COUNT
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_PERSON
                GROUP BY CLV_SEGMENT
                ORDER BY CUSTOMER_COUNT DESC
            """

            results = execute_query(query)

        return results if results else []


# Singleton instance for dependency injection
customer_segments_repository = CustomerSegmentsRepository()

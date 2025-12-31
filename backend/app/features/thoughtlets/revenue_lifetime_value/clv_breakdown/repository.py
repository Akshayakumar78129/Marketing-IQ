"""
Revenue & Lifetime Value - CLV Breakdown repository - Data access layer.
"""
from app.core.database import execute_query


class CLVBreakdownRepository:
    """Repository for CLV breakdown data access operations."""

    @staticmethod
    def get_clv_breakdown() -> dict:
        """
        Fetch overall CLV averages from DIM_PERSON.

        Returns:
            Dictionary with overall CLV averages (historic, predicted, total)
        """
        query = """
            SELECT
                AVG(HISTORIC_CLV) AS HISTORIC_CLV,
                AVG(PREDICTED_CLV) AS PREDICTED_CLV,
                AVG(TOTAL_CLV) AS TOTAL_CLV
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_PERSON
        """

        results = execute_query(query)
        return results[0] if results else {}


# Singleton instance for dependency injection
clv_breakdown_repository = CLVBreakdownRepository()

"""
Revenue & Lifetime Value - CLV Breakdown service - Business logic layer.
"""
from .repository import clv_breakdown_repository
from .models import CLVBreakdownResponse


class CLVBreakdownService:
    """Service class for CLV breakdown business logic."""

    def __init__(self, repository=clv_breakdown_repository):
        self.repository = repository

    def get_clv_breakdown(self) -> CLVBreakdownResponse:
        """
        Get overall CLV breakdown (averages).

        Returns:
            CLVBreakdownResponse with overall CLV averages
        """
        # Fetch data from repository
        data = self.repository.get_clv_breakdown()

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: dict) -> CLVBreakdownResponse:
        """Map database row to CLVBreakdownResponse."""
        return CLVBreakdownResponse(
            historic_clv=float(data.get("HISTORIC_CLV") or 0),
            predicted_clv=float(data.get("PREDICTED_CLV") or 0),
            total_clv=float(data.get("TOTAL_CLV") or 0)
        )


# Singleton instance for dependency injection
clv_breakdown_service = CLVBreakdownService()

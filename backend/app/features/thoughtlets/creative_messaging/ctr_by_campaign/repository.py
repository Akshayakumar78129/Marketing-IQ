"""
Creative & Messaging - CTR by Campaign repository - Data access layer.
"""
from datetime import date
from typing import Optional, List
from app.core.database import execute_query


class CTRByCampaignRepository:
    """Repository for CTR by campaign data access operations."""

    @staticmethod
    def get_ctr_by_campaign(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 10
    ) -> List[dict]:
        """
        Fetch top campaigns by CTR for bar chart.

        Args:
            date_from: Optional start date for filtering
            date_to: Optional end date for filtering
            limit: Maximum number of campaigns to return (default 10)

        Returns:
            List of dictionaries with campaign_name and ctr
        """
        date_conditions = []
        params = {"limit": limit}

        if date_from:
            date_conditions.append("date_day >= %(date_from)s::DATE")
            params["date_from"] = date_from.isoformat()

        if date_to:
            date_conditions.append("date_day <= %(date_to)s::DATE")
            params["date_to"] = date_to.isoformat()

        date_filter = ""
        if date_conditions:
            date_filter = "AND " + " AND ".join(date_conditions)

        query = f"""
            SELECT
                campaign_name AS CAMPAIGN_NAME,
                AVG(ctr) AS CTR
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE
            WHERE platform = 'meta'
            {date_filter}
            GROUP BY campaign_name
            ORDER BY CTR DESC
            LIMIT %(limit)s
        """

        results = execute_query(query, params)
        return results if results else []


# Singleton instance for dependency injection
ctr_by_campaign_repository = CTRByCampaignRepository()

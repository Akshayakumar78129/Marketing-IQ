"""
Meta Ads Device repository - Data access layer for device metrics.
"""
from datetime import date
from typing import Optional, List
from app.core.database import execute_query


class MetaAdsDeviceRepository:
    """Repository for Meta Ads device data access operations."""

    @staticmethod
    def get_devices(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        device: Optional[str] = None
    ) -> List[dict]:
        """
        Fetch Meta Ads device metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            device: Optional device filter

        Returns:
            List of dictionaries with device metrics
        """
        # Build filter conditions
        conditions = []
        params = {}

        if date_from:
            conditions.append("DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            conditions.append("DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        if device:
            conditions.append("DIMENSION_VALUE = %(device)s")
            params["device"] = device.lower()

        # Build filter clause
        filter_clause = ""
        if conditions:
            filter_clause = "AND " + " AND ".join(conditions)

        query = f"""
            SELECT
                DIMENSION_VALUE AS DEVICE,
                SUM(IMPRESSIONS) AS TOTAL_IMPRESSIONS,
                SUM(REACH) AS TOTAL_REACH,
                SUM(SPEND) AS TOTAL_SPEND,
                SUM(CLICKS) AS TOTAL_CLICKS,
                CASE WHEN SUM(IMPRESSIONS) > 0 THEN (SUM(CLICKS) / SUM(IMPRESSIONS)) * 100 ELSE 0 END AS CTR,
                CASE WHEN SUM(CLICKS) > 0 THEN SUM(SPEND) / SUM(CLICKS) ELSE 0 END AS CPC
            FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_META_DELIVERY
            WHERE PLATFORM = 'meta'
                AND DIMENSION_TYPE = 'device'
                {filter_clause}
            GROUP BY DIMENSION_VALUE
            ORDER BY TOTAL_SPEND DESC
        """

        results = execute_query(query, params if params else None)
        return results if results else []


# Singleton instance for dependency injection
meta_ads_device_repository = MetaAdsDeviceRepository()

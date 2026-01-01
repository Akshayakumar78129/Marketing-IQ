"""
Creative & Messaging - Creatives repository - Data access layer.
"""
from datetime import date
from typing import Optional, List, Tuple
from app.core.database import execute_query


class CreativesRepository:
    """Repository for creatives data access operations."""

    @staticmethod
    def get_creatives(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[List[dict], int]:
        """
        Fetch paginated creatives with performance data.

        Args:
            date_from: Optional start date for filtering
            date_to: Optional end date for filtering
            page: Page number (1-indexed)
            page_size: Number of items per page

        Returns:
            Tuple of (list of creative records, total count)
        """
        date_conditions = []
        params = {
            "page_size": page_size,
            "offset": (page - 1) * page_size
        }

        if date_from:
            date_conditions.append("p.date_day >= %(date_from)s::DATE")
            params["date_from"] = date_from.isoformat()

        if date_to:
            date_conditions.append("p.date_day <= %(date_to)s::DATE")
            params["date_to"] = date_to.isoformat()

        date_filter = ""
        if date_conditions:
            date_filter = "AND " + " AND ".join(date_conditions)

        query = f"""
            WITH creative_stats AS (
                SELECT
                    c.creative_id,
                    c.creative_name,
                    c.creative_type AS TYPE,
                    c.headline,
                    AVG(p.ctr) AS CTR,
                    SUM(p.impressions) AS IMPRESSIONS,
                    c.body_copy AS PRIMARY_TEXT,
                    c.status
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_CREATIVE c
                JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_AD a ON c.creative_id = a.creative_id
                JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_AD_PERFORMANCE p ON a.ad_id = p.ad_id
                WHERE a.platform = 'meta'
                {date_filter}
                GROUP BY c.creative_id, c.creative_name, c.creative_type, c.headline, c.body_copy, c.status
            ),
            total_count AS (
                SELECT COUNT(*) AS TOTAL FROM creative_stats
            )
            SELECT
                cs.creative_name AS CREATIVE_NAME,
                cs.TYPE,
                cs.headline AS HEADLINE,
                cs.CTR,
                cs.IMPRESSIONS,
                cs.PRIMARY_TEXT,
                cs.status AS STATUS,
                tc.TOTAL AS TOTAL_COUNT
            FROM creative_stats cs, total_count tc
            ORDER BY cs.IMPRESSIONS DESC NULLS LAST
            LIMIT %(page_size)s OFFSET %(offset)s
        """

        results = execute_query(query, params)

        if not results:
            return [], 0

        total = int(results[0].get("TOTAL_COUNT", 0)) if results else 0
        return results, total


# Singleton instance for dependency injection
creatives_repository = CreativesRepository()

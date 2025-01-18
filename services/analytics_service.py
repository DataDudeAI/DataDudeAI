from typing import Dict, List
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self, db):
        self.db = db
        
    def get_campaign_performance(self, campaign_id: int) -> Dict:
        """Get detailed campaign analytics"""
        try:
            return {
                'overview': self.db.get_campaign_stats(campaign_id),
                'conversions': self.db.get_campaign_conversions(campaign_id),
                'engagement': self.db.get_campaign_engagement(campaign_id),
                'demographics': self.db.get_campaign_demographics(campaign_id),
                'devices': self.db.get_campaign_devices(campaign_id),
                'locations': self.db.get_campaign_locations(campaign_id)
            }
        except Exception as e:
            logger.error(f"Error getting campaign performance: {str(e)}")
            return {}
            
    def get_social_analytics(self, team_id: int) -> Dict:
        """Get social media analytics"""
        try:
            return {
                'engagement_rate': self.db.get_social_engagement(team_id),
                'top_posts': self.db.get_top_performing_posts(team_id),
                'audience_growth': self.db.get_audience_growth(team_id),
                'platform_breakdown': self.db.get_platform_stats(team_id)
            }
        except Exception as e:
            logger.error(f"Error getting social analytics: {str(e)}")
            return {} 
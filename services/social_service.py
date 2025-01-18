from typing import Dict, List
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class SocialMediaService:
    def __init__(self, db):
        self.db = db
        
    def schedule_post(self, data: Dict) -> bool:
        """Schedule a social media post"""
        try:
            post_data = {
                'content': data['content'],
                'media_urls': json.dumps(data.get('media', [])),
                'platforms': json.dumps(data['platforms']),  # ['facebook', 'twitter', etc]
                'schedule_time': data['schedule_time'],
                'status': 'pending_approval',
                'team_id': data.get('team_id'),
                'created_by': data.get('user_id'),
                'campaign_id': data.get('campaign_id')
            }
            return self.db.create_social_post(post_data)
            
        except Exception as e:
            logger.error(f"Error scheduling post: {str(e)}")
            return False
            
    def get_content_calendar(self, team_id: int) -> List[Dict]:
        """Get content calendar for a team"""
        try:
            return self.db.get_social_posts(team_id)
        except Exception as e:
            logger.error(f"Error getting content calendar: {str(e)}")
            return []
            
    def approve_post(self, post_id: int, approver_id: int) -> bool:
        """Approve a social media post"""
        try:
            return self.db.update_post_status(post_id, 'approved', approver_id)
        except Exception as e:
            logger.error(f"Error approving post: {str(e)}")
            return False 
from typing import Dict, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MarketingService:
    def __init__(self, db):
        self.db = db
        
    def create_campaign(self, data: Dict) -> Optional[str]:
        """Create integrated marketing campaign"""
        try:
            campaign_data = {
                'name': data['name'],
                'type': data['type'],  # social, email, ads, etc.
                'platform': data.get('platform'),  # facebook, google, etc.
                'status': 'pending_approval',
                'budget': data.get('budget', 0),
                'start_date': data.get('start_date'),
                'end_date': data.get('end_date'),
                'targeting': json.dumps(data.get('targeting', {})),
                'creatives': json.dumps(data.get('creatives', [])),
                'goals': json.dumps(data.get('goals', {})),
                'team_id': data.get('team_id'),
                'created_by': data.get('user_id'),
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return self.db.create_campaign(campaign_data)
            
        except Exception as e:
            logger.error(f"Error creating campaign: {str(e)}")
            return None
            
    def schedule_social_post(self, data: Dict) -> bool:
        """Schedule social media post"""
        try:
            post_data = {
                'content': data['content'],
                'media_urls': json.dumps(data.get('media', [])),
                'platforms': json.dumps(data['platforms']),
                'schedule_time': data['schedule_time'],
                'campaign_id': data.get('campaign_id'),
                'status': 'pending_approval',
                'created_by': data.get('user_id'),
                'team_id': data.get('team_id')
            }
            
            return self.db.schedule_post(post_data)
            
        except Exception as e:
            logger.error(f"Error scheduling post: {str(e)}")
            return False
            
    def create_email_campaign(self, data: Dict) -> Optional[str]:
        """Create email marketing campaign"""
        try:
            email_data = {
                'subject': data['subject'],
                'content': data['content'],
                'template_id': data.get('template_id'),
                'list_id': data['list_id'],
                'schedule_time': data.get('schedule_time'),
                'status': 'pending_approval',
                'campaign_id': data.get('campaign_id'),
                'created_by': data.get('user_id'),
                'team_id': data.get('team_id')
            }
            
            return self.db.create_email_campaign(email_data)
            
        except Exception as e:
            logger.error(f"Error creating email campaign: {str(e)}")
            return None 
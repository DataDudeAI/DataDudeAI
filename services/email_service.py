from typing import Dict, List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self, db):
        self.db = db
        
    def create_campaign(self, data: Dict) -> Optional[int]:
        """Create email marketing campaign"""
        try:
            campaign_data = {
                'subject': data['subject'],
                'content': data['content'],
                'template_id': data.get('template_id'),
                'list_id': data['list_id'],
                'schedule_time': data.get('schedule_time'),
                'status': 'pending_approval',
                'team_id': data.get('team_id'),
                'created_by': data.get('user_id')
            }
            return self.db.create_email_campaign(campaign_data)
            
        except Exception as e:
            logger.error(f"Error creating email campaign: {str(e)}")
            return None
            
    def get_templates(self, team_id: int) -> List[Dict]:
        """Get email templates"""
        try:
            return self.db.get_email_templates(team_id)
        except Exception as e:
            logger.error(f"Error getting templates: {str(e)}")
            return [] 
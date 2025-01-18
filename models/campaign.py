from datetime import datetime
import uuid
import logging


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




class Campaign:
    def __init__(self, db):
        self.db = db

    def create_campaign(self, data):
        """Create new campaign"""
        try:
            campaign_data = {
                'name': data['name'],
                'original_url': data['url'],
                'type': data['type'],
                'short_code': self._generate_code(),
                'status': 'active',
                'utm_source': data.get('utm_source'),
                'utm_medium': data.get('utm_medium'),
                'utm_campaign': data.get('utm_campaign'),
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            if self.db.save_campaign(campaign_data):
                return campaign_data['short_code']
            return None
            
        except Exception as e:
            logger.error(f"Error creating campaign: {str(e)}")
            return None
    
    def _generate_code(self, length=8):
        """Generate unique short code"""
        return uuid.uuid4().hex[:length] 
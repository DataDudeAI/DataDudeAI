from typing import Dict, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ApprovalService:
    def __init__(self, db):
        self.db = db
        
    def create_approval_request(self, data: Dict) -> bool:
        """Create new approval request"""
        try:
            request_data = {
                'type': data['type'],  # campaign, post, email, etc
                'item_id': data['item_id'],
                'requester_id': data['user_id'],
                'team_id': data['team_id'],
                'status': 'pending',
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            return self.db.create_approval_request(request_data)
            
        except Exception as e:
            logger.error(f"Error creating approval request: {str(e)}")
            return False
            
    def get_pending_approvals(self, team_id: int) -> List[Dict]:
        """Get pending approval requests"""
        try:
            return self.db.get_approval_requests(team_id, status='pending')
        except Exception as e:
            logger.error(f"Error getting approvals: {str(e)}")
            return [] 
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class TeamService:
    def __init__(self, db):
        self.db = db
        
    def create_team(self, data: Dict) -> Optional[int]:
        """Create a new team"""
        try:
            team_data = {
                'name': data['name'],
                'org_id': data['org_id'],
                'settings': data.get('settings', {})
            }
            return self.db.create_team(team_data)
            
        except Exception as e:
            logger.error(f"Error creating team: {str(e)}")
            return None
            
    def add_member(self, team_id: int, user_data: Dict) -> bool:
        """Add member to team"""
        try:
            return self.db.add_team_member(team_id, user_data)
        except Exception as e:
            logger.error(f"Error adding team member: {str(e)}")
            return False 
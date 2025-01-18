from datetime import datetime
import hashlib
import json
from typing import Dict, Optional
import logging
from user_agents import parse

logger = logging.getLogger(__name__)

class TrackingService:
    def __init__(self, db, geo_service):
        self.db = db
        self.geo_service = geo_service
        
    def track_visit(self, request_data: Dict) -> bool:
        """Track a visit using only real request data"""
        try:
            # Extract only real data from the request
            client_info = {
                'ip_address': request_data.get('ip_address'),
                'user_agent': request_data.get('user_agent'),
                'referrer': request_data.get('referrer'),
                'session_id': request_data.get('session_id'),
                'campaign_code': request_data.get('campaign_code'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Enrich with real device and browser info
            enriched_data = self.geo_service.enrich_client_info(client_info)
            
            # Save to database
            return self.db.save_visit(enriched_data)
            
        except Exception as e:
            logger.error(f"Error tracking visit: {str(e)}")
            return False
            
    def track_event(self, request, event_type: str, event_data: Dict) -> bool:
        """Track custom events (conversions, interactions, etc.)"""
        try:
            session_id = request.cookies.get('session_id')
            visitor_id = self._generate_visitor_id(request)
            
            event = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'session_id': session_id,
                'visitor_id': visitor_id,
                'event_type': event_type,
                'event_data': event_data,
                'url': request.url,
                'referrer': request.referrer
            }
            
            return self.db.save_event(event)
            
        except Exception as e:
            logger.error(f"Error tracking event: {str(e)}")
            return False
            
    def _generate_visitor_id(self, request) -> str:
        """Generate unique visitor ID based on IP and user agent"""
        ip = request.remote_addr
        ua = request.headers.get('User-Agent', '')
        unique_str = f"{ip}-{ua}"
        return hashlib.md5(unique_str.encode()).hexdigest()
        
    def _get_device_type(self, user_agent) -> str:
        """Get detailed device type"""
        if user_agent.is_mobile:
            return 'mobile'
        elif user_agent.is_tablet:
            return 'tablet'
        elif user_agent.is_pc:
            return 'desktop'
        return 'other' 
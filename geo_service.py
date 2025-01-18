import logging
from datetime import datetime
from typing import Dict
from user_agents import parse

logger = logging.getLogger(__name__)

class GeoService:
    def enrich_client_info(self, client_info: Dict) -> Dict:
        """Enrich client info with device and browser data from user agent"""
        try:
            # Parse user agent string
            user_agent_string = client_info.get('user_agent', '')
            user_agent = parse(user_agent_string)
            
            # Extract real device info
            device_type = 'Mobile' if user_agent.is_mobile else (
                'Tablet' if user_agent.is_tablet else (
                'Bot' if user_agent.is_bot else 'Desktop'
            ))
            
            # Extract real OS info
            os = str(user_agent.os.family)
            os_version = str(user_agent.os.version_string)
            
            # Extract real browser info
            browser = str(user_agent.browser.family)
            browser_version = str(user_agent.browser.version_string)
            
            # Combine all data
            enriched_info = {
                **client_info,
                'device': {
                    'type': device_type,
                    'os': os,
                    'os_version': os_version
                },
                'browser': {
                    'family': browser,
                    'version': browser_version
                },
                'visit_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return enriched_info
            
        except Exception as e:
            logger.error(f"Error enriching client info: {str(e)}")
            return client_info 
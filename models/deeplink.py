from datetime import datetime
import json
from typing import Dict, Optional

class DeepLink:
    def __init__(self, db):
        self.db = db

    def create_deeplink(self, data: Dict) -> Optional[str]:
        """Create a new deep link"""
        try:
            link_data = {
                'short_code': self.generate_short_code(),
                'target_url': data.get('target_url'),
                'fallback_url': data.get('fallback_url'),
                'android_package': data.get('android_package'),
                'ios_bundle': data.get('ios_bundle'),
                'custom_data': json.dumps(data.get('custom_data', {})),
                'minimum_version': data.get('minimum_version'),
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'campaign_id': data.get('campaign_id'),
                'is_active': True
            }
            
            return self.db.save_deeplink(link_data)
            
        except Exception as e:
            print(f"Error creating deep link: {str(e)}")
            return None

    def generate_short_code(self) -> str:
        """Generate unique short code for deep link"""
        import uuid
        return f"dl-{str(uuid.uuid4())[:8]}"

    def build_dynamic_link(self, link_data: Dict) -> str:
        """Build dynamic link with all parameters"""
        base_url = "https://yourdomain.page.link"  # Replace with your domain
        params = {
            'link': link_data['target_url'],
            'apn': link_data.get('android_package', ''),
            'ibi': link_data.get('ios_bundle', ''),
            'isi': link_data.get('ios_store_id', ''),
            'ofl': link_data.get('fallback_url', ''),
            'min_version': link_data.get('minimum_version', ''),
            'data': link_data.get('custom_data', '{}')
        }
        return f"{base_url}/{link_data['short_code']}?{urlencode(params)}" 
import sqlite3
from datetime import datetime
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.db_path = "visits.db"
        self.initialize_db()

    def initialize_db(self):
        """Initialize database with all required tables"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Drop existing tables to reset schema
        #c.execute('DROP TABLE IF EXISTS visits')
        #c.execute('DROP TABLE IF EXISTS campaigns')
        
        # Create campaigns table
        c.execute('''
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                short_code TEXT UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                type TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                utm_source TEXT,
                utm_medium TEXT,
                utm_campaign TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create visits table with updated schema
        c.execute('''
            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_code TEXT,
                session_id TEXT,
                ip_address TEXT,
                user_agent TEXT,
                referrer TEXT,
                visit_data TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(campaign_code) REFERENCES campaigns(short_code)
            )
        ''')
        
        conn.commit()
        conn.close()

    def save_visit(self, visit_data):
        """Save only real visit data"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute('''
                INSERT INTO visits (
                    campaign_code, session_id, ip_address, 
                    user_agent, referrer, visit_data, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                visit_data.get('campaign_code'),
                visit_data.get('session_id'),
                visit_data.get('ip_address'),
                visit_data.get('user_agent'),
                visit_data.get('referrer'),
                json.dumps(visit_data),  # Store full enriched data as JSON
                visit_data.get('timestamp')
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Error saving visit: {str(e)}")
            return False

    def get_analytics(self):
        """Get analytics data"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            
            stats = {
                'total_visits': 0,
                'unique_visitors': 0,
                'bounce_rate': 0,
                'avg_time': 0,
                'states': {},
                'devices': {},
                'browsers': {},
                'isps': {},
                'recent_visits': [],
                'campaigns': {
                    'total': 0,
                    'active': 0,
                    'paused': 0,
                    'completed': 0
                }
            }
            
            # Get campaign counts
            c.execute('''
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active,
                    SUM(CASE WHEN status = 'paused' THEN 1 ELSE 0 END) as paused,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed
                FROM campaigns
            ''')
            campaign_stats = c.fetchone()
            stats['campaigns'] = {
                'total': campaign_stats['total'],
                'active': campaign_stats['active'] or 0,
                'paused': campaign_stats['paused'] or 0,
                'completed': campaign_stats['completed'] or 0
            }
            
            # Get total visits
            c.execute('SELECT COUNT(*) as count FROM visits')
            stats['total_visits'] = c.fetchone()['count']
            
            # Get unique visitors
            c.execute('SELECT COUNT(DISTINCT session_id) as count FROM visits')
            stats['unique_visitors'] = c.fetchone()['count']
            
            # Get visits with details
            c.execute('''
                SELECT v.*, c.name as campaign_name, c.type as campaign_type,
                       json_extract(v.visit_data, '$.state') as state,
                       json_extract(v.visit_data, '$.device.type') as device_type,
                       json_extract(v.visit_data, '$.browser.family') as browser,
                       json_extract(v.visit_data, '$.isp') as isp
                FROM visits v
                LEFT JOIN campaigns c ON v.campaign_code = c.short_code
                ORDER BY v.timestamp DESC
                LIMIT 100
            ''')
            
            visits = []
            for row in c.fetchall():
                visit = dict(row)
                visit_data = json.loads(visit.get('visit_data', '{}'))
                
                # Group by state
                state = visit_data.get('state', 'Unknown')
                stats['states'][state] = stats['states'].get(state, 0) + 1
                
                # Group by device
                device = visit_data.get('device', {}).get('type', 'Unknown')
                stats['devices'][device] = stats['devices'].get(device, 0) + 1
                
                # Group by browser
                browser = visit_data.get('browser', {}).get('family', 'Unknown')
                stats['browsers'][browser] = stats['browsers'].get(browser, 0) + 1
                
                # Group by ISP
                isp = visit_data.get('isp', 'Unknown')
                stats['isps'][isp] = stats['isps'].get(isp, 0) + 1
                
                # Add to visits list
                visits.append({
                    'timestamp': visit['timestamp'],
                    'campaign_name': visit['campaign_name'],
                    'campaign_type': visit['campaign_type'],
                    'visit_data': visit_data
                })
            
            # Get recent visits with campaign info
            c.execute('''
                SELECT 
                    v.*,
                    c.name as campaign_name,
                    c.type as campaign_type,
                    c.status as campaign_status
                FROM visits v
                LEFT JOIN campaigns c ON v.campaign_code = c.short_code
                ORDER BY v.timestamp DESC
                LIMIT 10
            ''')
            
            visits = []
            for row in c.fetchall():
                visit = dict(row)
                try:
                    visit['visit_data'] = json.loads(visit['visit_data'])
                except:
                    visit['visit_data'] = {}
                visits.append(visit)
            
            stats['recent_visits'] = visits
            
            conn.close()
            return stats
            
        except Exception as e:
            logger.error(f"Error getting analytics: {str(e)}")
            return {}

    def save_campaign(self, data):
        """Save new campaign"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute('''
                INSERT INTO campaigns (
                    name, short_code, original_url, type,
                    utm_source, utm_medium, utm_campaign
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['name'],
                data['short_code'],
                data['original_url'],
                data['type'],
                data.get('utm_source'),
                data.get('utm_medium'),
                data.get('utm_campaign')
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Error saving campaign: {str(e)}")
            return False

    def get_campaigns(self):
        """Get all campaigns with stats"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            
            c.execute('''
                SELECT c.*, 
                    COUNT(DISTINCT v.session_id) as unique_visitors,
                    COUNT(v.id) as total_clicks,
                    MAX(v.timestamp) as last_click
                FROM campaigns c
                LEFT JOIN visits v ON c.short_code = v.campaign_code
                GROUP BY c.id, c.short_code
                ORDER BY c.created_at DESC
            ''')
            
            campaigns = [dict(row) for row in c.fetchall()]
            conn.close()
            return campaigns
            
        except Exception as e:
            logger.error(f"Error getting campaigns: {str(e)}")
            return []

    def get_campaign(self, short_code):
        """Get campaign by short code"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            
            c.execute('''
                SELECT c.*, 
                    COUNT(DISTINCT v.session_id) as unique_visitors,
                    COUNT(v.id) as total_clicks
                FROM campaigns c
                LEFT JOIN visits v ON c.short_code = v.campaign_code
                WHERE c.short_code = ?
                GROUP BY c.id, c.short_code
            ''', (short_code,))
            
            row = c.fetchone()
            if row:
                campaign = dict(row)
                return campaign
                
            return None
            
        except Exception as e:
            logger.error(f"Error getting campaign: {str(e)}")
            return None 

    def update_campaign_stats(self, short_code, session_id):
        """Update campaign click stats"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Update total clicks and unique visitors
            c.execute('''
                UPDATE campaigns 
                SET 
                    total_clicks = total_clicks + 1,
                    unique_visitors = (
                        SELECT COUNT(DISTINCT session_id) 
                        FROM visits 
                        WHERE campaign_code = ?
                    )
                WHERE short_code = ?
            ''', (short_code, short_code))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error updating campaign stats: {str(e)}") 

    def save_deeplink(self, link_data):
        """Save new deep link"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute('''
                INSERT INTO deeplinks (
                    short_code, target_url, fallback_url, android_package,
                    ios_bundle, custom_data, minimum_version, campaign_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                link_data['short_code'],
                link_data['target_url'],
                link_data['fallback_url'],
                link_data['android_package'],
                link_data['ios_bundle'],
                link_data['custom_data'],
                link_data['minimum_version'],
                link_data['campaign_id']
            ))
            
            conn.commit()
            conn.close()
            return link_data['short_code']
            
        except Exception as e:
            logger.error(f"Error saving deep link: {str(e)}")
            return None

    def get_deeplink(self, short_code):
        """Get deep link by short code"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute('SELECT * FROM deeplinks WHERE short_code = ?', (short_code,))
            row = c.fetchone()
            
            if row:
                columns = [col[0] for col in c.description]
                link_data = dict(zip(columns, row))
                link_data['custom_data'] = json.loads(link_data['custom_data'])
                return link_data
                
            return None
            
        except Exception as e:
            logger.error(f"Error getting deep link: {str(e)}")
            return None 

    def get_visits(self):
        """Get all visits with full details"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            
            c.execute('''
                SELECT v.*, c.name, c.type as campaign_type 
                FROM visits v
                LEFT JOIN campaigns c ON v.campaign_code = c.short_code
                ORDER BY v.timestamp DESC
            ''')
            
            visits = []
            for row in c.fetchall():
                visit = dict(row)
                try:
                    visit_data = json.loads(visit.get('visit_data', '{}'))
                    visit.update(visit_data)
                except:
                    pass
                visits.append(visit)
                
            conn.close()
            return visits
            
        except Exception as e:
            logger.error(f"Error getting visits: {str(e)}")
            return [] 

    def update_campaign(self, short_code, data):
        """Update existing campaign"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute('''
                UPDATE campaigns 
                SET name = ?, original_url = ?, status = ?
                WHERE short_code = ?
            ''', (data['name'], data['url'], data['status'], short_code))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Error updating campaign: {str(e)}")
            return False

    def delete_campaign(self, short_code):
        """Delete campaign"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute('DELETE FROM campaigns WHERE short_code = ?', (short_code,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Error deleting campaign: {str(e)}")
            return False 
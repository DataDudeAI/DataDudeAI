from flask import Flask, request, render_template, jsonify, session, redirect
from datetime import datetime
from geo_service import GeoService
from database import Database
from models.campaign import Campaign
from models.deeplink import DeepLink
from user_agents import parse
import logging
import uuid

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production
geo_service = GeoService()
db = Database()

@app.before_request
def before_request():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track', methods=['POST'])
def track_visitor():
    client_info = {
        'ip_address': request.remote_addr,
        'user_agent': request.headers.get('User-Agent'),
        'referrer': request.referrer,
        'session_id': session.get('user_id'),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    enriched_data = geo_service.enrich_client_info(client_info)
    db.save_visit(enriched_data)
    return jsonify(enriched_data)

@app.route('/analytics')
def analytics():
    stats = db.get_analytics()
    return render_template('analytics.html', stats=stats)

@app.route('/api/stats')
def get_stats():
    """Get analytics stats"""
    try:
        stats = db.get_analytics()
        if not stats:
            stats = {
                'total_visits': 0,
                'unique_visitors': 0,
                'bounce_rate': 0,
                'avg_time': 0,
                'states': {},
                'devices': {},
                'browsers': {},
                'isps': {},
                'recent_visits': []
            }
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({
            'error': str(e),
            'total_visits': 0,
            'unique_visitors': 0,
            'bounce_rate': 0,
            'avg_time': 0,
            'states': {},
            'devices': {},
            'browsers': {},
            'isps': {},
            'recent_visits': []
        })

@app.route('/campaign/create', methods=['GET', 'POST'])
def create_campaign():
    """Create new campaign"""
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            campaign = Campaign(db)
            short_code = campaign.create_campaign(data)
            
            if short_code:
                return jsonify({
                    'success': True,
                    'short_code': short_code,
                    'short_url': request.host_url + short_code
                })
            return jsonify({'success': False, 'error': 'Failed to create campaign'})
            
        except Exception as e:
            logger.error(f"Error creating campaign: {str(e)}")
            return jsonify({'success': False, 'error': str(e)})
            
    # GET request - show the form
    return render_template('campaign_create.html')

@app.route('/campaigns')
def list_campaigns():
    """List all campaigns"""
    campaigns = db.get_campaigns()
    return render_template('campaigns.html', campaigns=campaigns)

@app.route('/<short_code>')
def redirect_url(short_code):
    campaign = db.get_campaign(short_code)
    if campaign:
        # Record visit
        client_info = {
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'referrer': request.referrer,
            'session_id': session.get('user_id'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'campaign_code': short_code
        }
        enriched_data = geo_service.enrich_client_info(client_info)
        db.save_visit(enriched_data)
        
        # Build redirect URL with UTM parameters
        url = campaign['original_url']
        utm_params = {
            'utm_source': campaign.get('utm_source'),
            'utm_medium': campaign.get('utm_medium'),
            'utm_campaign': campaign.get('utm_campaign')
        }
        
        # Add UTM parameters if they exist
        utm_string = '&'.join([f"{k}={v}" for k, v in utm_params.items() if v])
        if utm_string:
            separator = '?' if '?' not in url else '&'
            url = f"{url}{separator}{utm_string}"
            
        return redirect(url)
        
    return "Link not found", 404

@app.route('/dl/create', methods=['GET', 'POST'])
def create_deeplink():
    if request.method == 'POST':
        deeplink = DeepLink(db)
        short_code = deeplink.create_deeplink(request.form)
        if short_code:
            return jsonify({
                'success': True,
                'short_code': short_code,
                'deep_link': request.host_url + 'dl/' + short_code
            })
        return jsonify({'success': False, 'error': 'Failed to create deep link'})
    
    return render_template('deeplink_create.html')

@app.route('/dl/<short_code>')
def handle_deeplink(short_code):
    link_data = db.get_deeplink(short_code)
    if not link_data:
        return "Link not found", 404
        
    # Parse user agent
    user_agent = parse(request.headers.get('User-Agent', ''))
    
    # Record visit
    client_info = {
        'ip_address': request.remote_addr,
        'user_agent': request.headers.get('User-Agent'),
        'referrer': request.referrer,
        'session_id': session.get('user_id'),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'deeplink_code': short_code
    }
    enriched_data = geo_service.enrich_client_info(client_info)
    db.save_visit(enriched_data)
    
    # Determine redirect URL based on device
    if user_agent.is_mobile:
        if user_agent.os.family == 'iOS' and link_data['ios_bundle']:
            return redirect(f"itms-apps://itunes.apple.com/app/{link_data['ios_bundle']}")
        elif user_agent.os.family == 'Android' and link_data['android_package']:
            return redirect(f"market://details?id={link_data['android_package']}")
            
    # Fallback to web URL
    return redirect(link_data['fallback_url'] or link_data['target_url'])

@app.route('/api/campaigns')
def get_campaigns():
    """Get all campaigns"""
    campaigns = db.get_campaigns()
    return jsonify(campaigns)

@app.route('/api/campaigns/<short_code>')
def get_campaign(short_code):
    """Get specific campaign"""
    campaign = db.get_campaign(short_code)
    if campaign:
        return jsonify(campaign)
    return jsonify({'error': 'Campaign not found'}), 404

@app.route('/api/campaigns/<short_code>', methods=['PUT'])
def update_campaign(short_code):
    """Update campaign"""
    try:
        data = request.form.to_dict()
        if db.update_campaign(short_code, data):
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Failed to update campaign'})
    except Exception as e:
        logger.error(f"Error updating campaign: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/campaigns/<short_code>', methods=['DELETE'])
def delete_campaign(short_code):
    """Delete campaign"""
    try:
        if db.delete_campaign(short_code):
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Failed to delete campaign'})
    except Exception as e:
        logger.error(f"Error deleting campaign: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True) 
document.addEventListener('DOMContentLoaded', function() {
    showLoadingState();
    fetchAndUpdateStats();
    // Refresh stats every 30 seconds
    setInterval(fetchAndUpdateStats, 30000);
});

function showLoadingState() {
    const loadingHtml = `
        <div class="loading-spinner">
            <div class="spinner"></div>
            <div>Loading data...</div>
        </div>
    `;
    
    document.querySelectorAll('.chart').forEach(chart => {
        chart.innerHTML = loadingHtml;
    });
}

function fetchAndUpdateStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showErrorState(data.error);
                return;
            }
            updateDashboard(data);
        })
        .catch(error => {
            console.error('Error fetching stats:', error);
            showErrorState(error);
        });
}

function updateDashboard(data) {
    // Update summary stats with animations
    updateElement('total-visits', data.total_visits || 0);
    updateElement('unique-visitors', data.unique_visitors || 0);
    updateElement('bounce-rate', (data.bounce_rate || 0) + '%');
    updateElement('avg-time', formatTime(data.avg_time || 0));
    
    // Create charts
    createLocationChart(data.states || {});
    createDeviceChart(data.devices || {});
    createBrowserChart(data.browsers || {});
    createISPChart(data.isps || {});
    
    // Update timeline
    updateTimeline(data.recent_visits || []);
}

function updateElement(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = value;
    }
}

function formatTime(seconds) {
    if (!seconds) return '0s';
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.round(seconds % 60);
    return minutes > 0 ? `${minutes}m ${remainingSeconds}s` : `${remainingSeconds}s`;
}

function updateTimeline(visits) {
    const timeline = document.getElementById('recent-visits');
    if (!timeline) return;
    
    if (!visits || !visits.length) {
        timeline.innerHTML = '<div class="no-data">No recent visits</div>';
        return;
    }
    
    const html = visits.map(visit => {
        const visitData = visit.visit_data || {};
        const device = visitData.device || {};
        const browser = visitData.browser || {};
        
        return `
            <div class="timeline-item">
                <div class="timeline-icon">
                    <i class="fas ${getDeviceIcon(device.type)}"></i>
                </div>
                <div class="timeline-content">
                    <div class="timeline-header">
                        <span class="timeline-campaign badge badge-${visit.campaign_type || 'default'}">
                            ${visit.campaign_name || 'Unknown Campaign'}
                        </span>
                        <span class="timeline-time">${formatTimeAgo(visit.timestamp)}</span>
                    </div>
                    <div class="timeline-details">
                        <div class="device-info">
                            <i class="fas fa-microchip"></i>
                            ${device.type || 'Unknown Device'} • 
                            ${device.os || 'Unknown OS'} ${device.os_version || ''}
                        </div>
                        <div class="browser-info">
                            <i class="fas fa-globe"></i>
                            ${browser.family || 'Unknown Browser'} ${browser.version || ''}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    timeline.innerHTML = html;
}

function getDeviceIcon(deviceType) {
    switch(deviceType?.toLowerCase()) {
        case 'mobile':
            return 'fa-mobile-alt';
        case 'tablet':
            return 'fa-tablet-alt';
        case 'desktop':
            return 'fa-desktop';
        case 'bot':
            return 'fa-robot';
        default:
            return 'fa-question-circle';
    }
}

function formatTimeAgo(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);

    if (seconds < 60) {
        return 'just now';
    }
    
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) {
        return `${minutes}m ago`;
    }
    
    const hours = Math.floor(minutes / 60);
    if (hours < 24) {
        return `${hours}h ago`;
    }
    
    const days = Math.floor(hours / 24);
    if (days < 7) {
        return `${days}d ago`;
    }
    
    return date.toLocaleDateString();
}

function createLocationChart(data) {
    const chart = document.getElementById('location-chart');
    if (!chart) return;
    
    if (!Object.keys(data).length) {
        chart.innerHTML = '<div class="no-data">No location data available</div>';
        return;
    }
    
    const chartData = [{
        values: Object.values(data),
        labels: Object.keys(data),
        type: 'pie',
        hole: 0.4
    }];
    
    const layout = {
        margin: { t: 20, b: 20, l: 20, r: 20 },
        showlegend: true,
        legend: { orientation: 'h' }
    };
    
    Plotly.newPlot('location-chart', chartData, layout);
}

function createDeviceChart(data) {
    const chart = document.getElementById('device-chart');
    if (!chart) return;
    
    if (!Object.keys(data).length) {
        chart.innerHTML = '<div class="no-data">No device data available</div>';
        return;
    }
    
    const chartData = [{
        values: Object.values(data),
        labels: Object.keys(data),
        type: 'pie',
        hole: 0.4
    }];
    
    const layout = {
        margin: { t: 20, b: 20, l: 20, r: 20 },
        showlegend: true,
        legend: { orientation: 'h' }
    };
    
    Plotly.newPlot('device-chart', chartData, layout);
}

function createBrowserChart(data) {
    const chart = document.getElementById('browser-chart');
    if (!chart) return;
    
    if (!Object.keys(data).length) {
        chart.innerHTML = '<div class="no-data">No browser data available</div>';
        return;
    }
    
    const chartData = [{
        values: Object.values(data),
        labels: Object.keys(data),
        type: 'pie',
        hole: 0.4
    }];
    
    const layout = {
        margin: { t: 20, b: 20, l: 20, r: 20 },
        showlegend: true,
        legend: { orientation: 'h' }
    };
    
    Plotly.newPlot('browser-chart', chartData, layout);
}

function createISPChart(data) {
    const chart = document.getElementById('isp-chart');
    if (!chart) return;
    
    if (!Object.keys(data).length) {
        chart.innerHTML = '<div class="no-data">No ISP data available</div>';
        return;
    }
    
    const chartData = [{
        values: Object.values(data),
        labels: Object.keys(data),
        type: 'pie',
        hole: 0.4
    }];
    
    const layout = {
        margin: { t: 20, b: 20, l: 20, r: 20 },
        showlegend: true,
        legend: { orientation: 'h' }
    };
    
    Plotly.newPlot('isp-chart', chartData, layout);
}

function showErrorState(error) {
    const errorHtml = `
        <div class="error-message">
            <i class="fas fa-exclamation-circle"></i>
            <div>Failed to load data: ${error}</div>
        </div>
    `;
    
    document.querySelectorAll('.chart').forEach(chart => {
        chart.innerHTML = errorHtml;
    });
}

// Load stats when page loads
document.addEventListener('DOMContentLoaded', loadStats); 
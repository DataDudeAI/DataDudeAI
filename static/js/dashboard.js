document.addEventListener('DOMContentLoaded', function() {
    fetchAndUpdateDashboard();
    // Refresh every 30 seconds
    setInterval(fetchAndUpdateDashboard, 30000);
});

function fetchAndUpdateDashboard() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            updateStats(data);
            createMiniCharts(data);
            updateRecentActivity(data.recent_visits);
        })
        .catch(error => {
            console.error('Error:', error);
            showErrorMessage('Failed to load dashboard data');
        });
}

function showErrorMessage(message) {
    const container = document.querySelector('.dashboard-container');
    if (container) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `
            <i class="fas fa-exclamation-circle"></i>
            <p>${message}</p>
        `;
        container.prepend(errorDiv);
        setTimeout(() => errorDiv.remove(), 5000);
    }
}

function updateStats(data) {
    // Update visitor stats
    updateStatValue('total-visitors', data.total_visits || 0);
    updateStatValue('unique-visitors', data.unique_visitors || 0);
    
    // Update campaign stats
    updateStatValue('total-campaigns', data.campaigns?.total || 0);
    updateStatValue('active-campaigns', data.campaigns?.active || 0);
    
    // Update other stats if needed
    updateStatValue('bounce-rate', (data.bounce_rate || 0) + '%');
    updateStatValue('avg-time', formatTime(data.avg_time || 0));
}

function updateStatValue(elementId, value) {
    const element = document.getElementById(elementId);
    if (element) {
        // Add animation class if needed
        element.classList.add('animate-value');
        element.textContent = value;
        setTimeout(() => element.classList.remove('animate-value'), 500);
    }
}

function formatTime(seconds) {
    if (!seconds) return '0s';
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.round(seconds % 60);
    return minutes > 0 ? `${minutes}m ${remainingSeconds}s` : `${remainingSeconds}s`;
}

function createMiniCharts(data) {
    // Visitors by State Chart
    const stateData = {
        values: Object.values(data.states),
        labels: Object.keys(data.states),
        type: 'pie',
        hole: 0.4,
        marker: {
            colors: generateColors(Object.keys(data.states).length)
        }
    };

    Plotly.newPlot('mini-visitors-chart', [stateData], {
        margin: {t: 0, b: 0, l: 0, r: 0},
        showlegend: false,
        height: 150
    });

    // Devices Chart
    const deviceData = {
        values: Object.values(data.devices),
        labels: Object.keys(data.devices),
        type: 'pie',
        hole: 0.4,
        marker: {
            colors: generateColors(Object.keys(data.devices).length)
        }
    };

    Plotly.newPlot('mini-platforms-chart', [deviceData], {
        margin: {t: 0, b: 0, l: 0, r: 0},
        showlegend: false,
        height: 150
    });
}

function updateRecentActivity(visits) {
    const activityList = document.getElementById('recent-activities');
    if (!visits || !visits.length) {
        activityList.innerHTML = '<div class="no-data">No recent activity</div>';
        return;
    }

    activityList.innerHTML = visits.map(visit => {
        const visitData = visit.visit_data || {};
        const device = visitData.device || {};
        const browser = visitData.browser || {};
        
        return `
            <div class="activity-item">
                <div class="activity-icon">
                    <i class="fas ${getDeviceIcon(device.type)}"></i>
                </div>
                <div class="activity-content">
                    <div class="activity-header">
                        <span class="activity-campaign">${visit.campaign_name || 'Unknown Campaign'}</span>
                        <span class="activity-time">${formatTimeAgo(visit.timestamp)}</span>
                    </div>
                    <div class="activity-details">
                        <span class="device-info">
                            ${device.type || 'Unknown Device'} • ${device.os || 'Unknown OS'}
                        </span>
                        <span class="browser-info">
                            ${browser.family || 'Unknown Browser'} ${browser.version || ''}
                        </span>
                    </div>
                </div>
            </div>
        `;
    }).join('');
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

function generateColors(count) {
    const colors = [];
    for (let i = 0; i < count; i++) {
        colors.push(getRandomColor());
    }
    return colors;
}

function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
} 
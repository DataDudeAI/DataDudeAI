document.addEventListener('DOMContentLoaded', function() {
    loadCampaigns();
    
    // Form submission
    document.getElementById('campaign-form').addEventListener('submit', function(e) {
        e.preventDefault();
        createCampaign(this);
    });
    
    // Edit form submission
    document.getElementById('edit-form').addEventListener('submit', function(e) {
        e.preventDefault();
        updateCampaign(this);
    });
    
    // Modal close button
    document.querySelector('.close').addEventListener('click', function() {
        document.getElementById('edit-modal').style.display = 'none';
    });
});

function loadCampaigns() {
    fetch('/api/campaigns')
        .then(response => response.json())
        .then(campaigns => {
            const tbody = document.getElementById('campaigns-body');
            tbody.innerHTML = campaigns.map(campaign => `
                <tr>
                    <td>${escapeHtml(campaign.name)}</td>
                    <td>
                        <a href="/${campaign.short_code}" target="_blank" class="campaign-url">
                            ${window.location.host}/${campaign.short_code}
                            <i class="fas fa-external-link-alt"></i>
                        </a>
                        <button onclick="copyUrl('${campaign.short_code}')" class="btn-icon copy">
                            <i class="fas fa-copy"></i>
                        </button>
                    </td>
                    <td>
                        <span class="badge badge-${campaign.type}">
                            ${campaign.type}
                        </span>
                    </td>
                    <td>${campaign.total_clicks || 0}</td>
                    <td>${campaign.unique_visitors || 0}</td>
                    <td>${formatDate(campaign.created_at)}</td>
                    <td>
                        <span class="status-badge ${campaign.status}">
                            ${campaign.status}
                        </span>
                    </td>
                    <td class="actions">
                        <button onclick="editCampaign('${campaign.short_code}')" class="btn-icon">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button onclick="deleteCampaign('${campaign.short_code}')" class="btn-icon delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `).join('');
        })
        .catch(error => {
            console.error('Error loading campaigns:', error);
            showNotification('Error loading campaigns', 'error');
        });
}

function createCampaign(form) {
    const formData = new FormData(form);
    
    // Add required fields if missing
    if (!formData.get('name')) {
        showNotification('Campaign name is required', 'error');
        return;
    }
    if (!formData.get('url')) {
        showNotification('URL is required', 'error');
        return;
    }
    if (!formData.get('type')) {
        formData.set('type', 'general');
    }
    
    fetch('/campaign/create', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            form.reset();
            loadCampaigns();
            showNotification('Campaign created successfully!');
        } else {
            showNotification(data.error || 'Error creating campaign', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error creating campaign', 'error');
    });
}

function editCampaign(shortCode) {
    fetch(`/api/campaigns/${shortCode}`)
        .then(response => response.json())
        .then(campaign => {
            const form = document.getElementById('edit-form');
            form.campaign_id.value = campaign.short_code;
            form.name.value = campaign.name;
            form.url.value = campaign.original_url;
            form.status.value = campaign.status;
            
            document.getElementById('edit-modal').style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error loading campaign', 'error');
        });
}

function updateCampaign(form) {
    const formData = new FormData(form);
    const shortCode = formData.get('campaign_id');
    
    fetch(`/api/campaigns/${shortCode}`, {
        method: 'PUT',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('edit-modal').style.display = 'none';
            loadCampaigns();
            showNotification('Campaign updated successfully!');
        } else {
            showNotification(data.error || 'Error updating campaign', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error updating campaign', 'error');
    });
}

function deleteCampaign(shortCode) {
    if (confirm('Are you sure you want to delete this campaign?')) {
        fetch(`/api/campaigns/${shortCode}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadCampaigns();
                showNotification('Campaign deleted successfully!');
            } else {
                showNotification(data.error || 'Error deleting campaign', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error deleting campaign', 'error');
        });
    }
}

function showNotification(message, type = 'success') {
    // Implementation of notification system
    alert(message);
}

// Helper functions
function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function copyUrl(shortCode) {
    const url = `${window.location.origin}/${shortCode}`;
    navigator.clipboard.writeText(url)
        .then(() => showNotification('URL copied to clipboard!'))
        .catch(() => showNotification('Failed to copy URL', 'error'));
} 
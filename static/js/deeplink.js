document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('deeplink-form');
    const resultBox = document.getElementById('result');
    const shortUrlSpan = document.getElementById('deep-link');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        
        // Validate custom data JSON
        try {
            const customData = formData.get('custom_data');
            if (customData) {
                JSON.parse(customData);
            }
        } catch (e) {
            alert('Invalid JSON in custom data field');
            return;
        }

        fetch('/dl/create', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                shortUrlSpan.textContent = data.deep_link;
                shortUrlSpan.href = data.deep_link;
                resultBox.style.display = 'block';
                
                // Add copy button functionality
                const copyBtn = document.getElementById('copy-link');
                copyBtn.addEventListener('click', () => {
                    navigator.clipboard.writeText(data.deep_link);
                    copyBtn.textContent = 'Copied!';
                    setTimeout(() => copyBtn.textContent = 'Copy Link', 2000);
                });
                
                form.reset();
            } else {
                alert('Failed to create link: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while creating the link');
        });
    });
}); 
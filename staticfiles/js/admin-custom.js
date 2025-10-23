// Custom Admin JavaScript for আমার ফ্রেশ বিডি

document.addEventListener('DOMContentLoaded', function() {
    console.log('আমার ফ্রেশ বিডি Admin loaded');
    
    // Add Bengali font class to body
    document.body.classList.add('bengali-text');
    
    // Enhanced image preview functionality
    setupImagePreviews();
    
    // Auto-save functionality for forms
    setupAutoSave();
    
    // Enhanced search functionality
    setupEnhancedSearch();
    
    // Dashboard enhancements
    setupDashboardEnhancements();
});

function setupImagePreviews() {
    // Add hover effects to product images
    const productImages = document.querySelectorAll('.field-display_image img');
    productImages.forEach(img => {
        img.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
            this.style.transition = 'transform 0.2s ease';
        });
        
        img.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // Image upload preview
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Create or update preview
                    let preview = input.parentNode.querySelector('.image-preview');
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.className = 'image-preview';
                        preview.style.cssText = 'max-width: 200px; max-height: 200px; margin-top: 10px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);';
                        input.parentNode.appendChild(preview);
                    }
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });
}

function setupAutoSave() {
    // Auto-save draft functionality for long forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                // Save to localStorage as draft
                const formId = form.id || 'admin-form';
                const drafts = JSON.parse(localStorage.getItem('admin-drafts') || '{}');
                drafts[formId] = drafts[formId] || {};
                drafts[formId][input.name] = input.value;
                localStorage.setItem('admin-drafts', JSON.stringify(drafts));
                
                // Show save indicator
                showSaveIndicator('Draft saved');
            });
        });
    });
}

function setupEnhancedSearch() {
    // Enhanced search with suggestions
    const searchInputs = document.querySelectorAll('input[name="q"]');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const query = this.value;
            if (query.length > 2) {
                // Add search suggestions (you can implement AJAX here)
                console.log('Searching for:', query);
            }
        });
    });
}

function setupDashboardEnhancements() {
    // Add dashboard statistics if on dashboard page
    if (window.location.pathname.includes('/admin/') && window.location.pathname.endsWith('/admin/')) {
        addDashboardStats();
    }
}

function addDashboardStats() {
    // This would typically fetch data via AJAX
    const dashboardContent = document.querySelector('#content-main');
    if (dashboardContent) {
        const statsHTML = `
            <div class="dashboard-stats">
                <div class="stat-card">
                    <h3 id="total-products">-</h3>
                    <p>Total Products</p>
                </div>
                <div class="stat-card">
                    <h3 id="total-orders">-</h3>
                    <p>Total Orders</p>
                </div>
                <div class="stat-card">
                    <h3 id="total-revenue">৳-</h3>
                    <p>Total Revenue</p>
                </div>
                <div class="stat-card">
                    <h3 id="low-stock">-</h3>
                    <p>Low Stock Items</p>
                </div>
            </div>
        `;
        
        dashboardContent.insertAdjacentHTML('afterbegin', statsHTML);
        
        // Load actual stats (this would be from your dashboard callback)
        loadDashboardStats();
    }
}

function loadDashboardStats() {
    // This would typically be populated by the dashboard_callback function
    // For now, we'll use placeholder values
    setTimeout(() => {
        document.getElementById('total-products').textContent = '150';
        document.getElementById('total-orders').textContent = '45';
        document.getElementById('total-revenue').textContent = '৳25,000';
        document.getElementById('low-stock').textContent = '8';
    }, 500);
}

function showSaveIndicator(message) {
    // Show a temporary save indicator
    let indicator = document.getElementById('save-indicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'save-indicator';
        indicator.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #10b981;
            color: white;
            padding: 8px 16px;
            border-radius: 4px;
            font-size: 14px;
            z-index: 9999;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;
        document.body.appendChild(indicator);
    }
    
    indicator.textContent = message;
    indicator.style.opacity = '1';
    
    setTimeout(() => {
        indicator.style.opacity = '0';
    }, 2000);
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('bn-BD', {
        style: 'currency',
        currency: 'BDT',
        minimumFractionDigits: 0
    }).format(amount);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('bn-BD', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

// Export functions for use in other scripts
window.AdminCustom = {
    showSaveIndicator,
    formatCurrency,
    formatDate
};
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
// D
ashboard specific JavaScript
function initializeDashboard() {
    // Add smooth animations to dashboard cards
    const dashboardCards = document.querySelectorAll('.dashboard-card');
    dashboardCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Add click tracking for quick actions
    const quickActions = document.querySelectorAll('.dashboard-quick-action');
    quickActions.forEach(action => {
        action.addEventListener('click', function(e) {
            // Track click analytics (you can send to your analytics service)
            console.log('Quick action clicked:', this.textContent.trim());
        });
    });
    
    // Auto-refresh dashboard stats every 5 minutes
    setInterval(refreshDashboardStats, 5 * 60 * 1000);
}

function refreshDashboardStats() {
    // This would typically make an AJAX call to refresh stats
    console.log('Refreshing dashboard stats...');
    
    // Add loading state to stat cards
    const statValues = document.querySelectorAll('.dashboard-stat-value');
    statValues.forEach(stat => {
        stat.style.opacity = '0.6';
    });
    
    // Simulate API call
    setTimeout(() => {
        statValues.forEach(stat => {
            stat.style.opacity = '1';
        });
        showSaveIndicator('Dashboard updated');
    }, 1000);
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.dashboard-card')) {
        initializeDashboard();
    }
});

// Add keyboard shortcuts for common admin actions
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Shift + A = Add new product
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'A') {
        e.preventDefault();
        const addProductLink = document.querySelector('a[href*="product/add"]');
        if (addProductLink) {
            window.location.href = addProductLink.href;
        }
    }
    
    // Ctrl/Cmd + Shift + O = View orders
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'O') {
        e.preventDefault();
        const ordersLink = document.querySelector('a[href*="order/"]');
        if (ordersLink) {
            window.location.href = ordersLink.href;
        }
    }
    
    // Ctrl/Cmd + Shift + D = Dashboard
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'D') {
        e.preventDefault();
        window.location.href = '/admin/';
    }
});

// Add tooltips to dashboard elements
function addDashboardTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function(e) {
            const tooltip = document.createElement('div');
            tooltip.className = 'dashboard-tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');
            tooltip.style.cssText = `
                position: absolute;
                background: #1f2937;
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 12px;
                z-index: 1000;
                pointer-events: none;
                opacity: 0;
                transition: opacity 0.2s ease;
            `;
            
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
            
            setTimeout(() => tooltip.style.opacity = '1', 10);
            
            this.addEventListener('mouseleave', function() {
                tooltip.remove();
            }, { once: true });
        });
    });
}

// Initialize tooltips when DOM is loaded
document.addEventListener('DOMContentLoaded', addDashboardTooltips);// C
hart.js Dashboard Enhancements
function initializeCharts() {
    // Set Chart.js global defaults
    if (typeof Chart !== 'undefined') {
        Chart.defaults.font.family = 'Inter, system-ui, sans-serif';
        Chart.defaults.color = '#6b7280';
        Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(0, 0, 0, 0.8)';
        Chart.defaults.plugins.tooltip.titleColor = '#ffffff';
        Chart.defaults.plugins.tooltip.bodyColor = '#ffffff';
        Chart.defaults.plugins.tooltip.cornerRadius = 6;
        Chart.defaults.plugins.tooltip.padding = 12;
    }
}

// Chart utility functions
function formatCurrencyForChart(value) {
    return '৳' + new Intl.NumberFormat('en-BD').format(value);
}

function getChartColors() {
    return {
        primary: '#3b82f6',
        success: '#10b981',
        warning: '#f59e0b',
        danger: '#ef4444',
        purple: '#8b5cf6',
        indigo: '#6366f1',
        pink: '#ec4899',
        gray: '#6b7280'
    };
}

// Chart animation helpers
function animateChart(chart) {
    chart.update('active');
}

// Chart refresh functionality
function refreshChartData(chartId, newData, newLabels) {
    const chart = Chart.getChart(chartId);
    if (chart) {
        chart.data.labels = newLabels;
        chart.data.datasets[0].data = newData;
        chart.update('active');
    }
}

// Chart export functionality
function exportChartAsImage(chartId, filename) {
    const chart = Chart.getChart(chartId);
    if (chart) {
        const url = chart.toBase64Image();
        const link = document.createElement('a');
        link.download = filename || 'chart.png';
        link.href = url;
        link.click();
    }
}

// Chart resize handler
function handleChartResize() {
    Chart.helpers.each(Chart.instances, function(chart) {
        chart.resize();
    });
}

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    
    // Handle window resize for charts
    window.addEventListener('resize', handleChartResize);
});

// Chart interaction enhancements
function addChartInteractions() {
    // Add click handlers for chart elements
    const chartContainers = document.querySelectorAll('.chart-container');
    chartContainers.forEach(container => {
        const canvas = container.querySelector('canvas');
        if (canvas) {
            canvas.addEventListener('click', function(event) {
                const chart = Chart.getChart(canvas);
                if (chart) {
                    const points = chart.getElementsAtEventForMode(event, 'nearest', { intersect: true }, true);
                    if (points.length) {
                        const firstPoint = points[0];
                        const label = chart.data.labels[firstPoint.index];
                        const value = chart.data.datasets[firstPoint.datasetIndex].data[firstPoint.index];
                        console.log('Chart clicked:', { label, value });
                        
                        // You can add custom actions here
                        // For example, navigate to detailed view
                    }
                }
            });
        }
    });
}

// Chart data update via AJAX
function updateDashboardCharts() {
    // This would typically fetch new data from your Django backend
    fetch('/admin/dashboard-data/', {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        // Update each chart with new data
        if (data.sales_data) {
            refreshChartData('salesChart', data.sales_data, data.sales_labels);
        }
        if (data.order_status_data) {
            refreshChartData('orderStatusChart', data.order_status_data, data.order_status_labels);
        }
        // Add more chart updates as needed
        
        showSaveIndicator('Charts updated');
    })
    .catch(error => {
        console.error('Error updating charts:', error);
    });
}

// Auto-refresh charts every 5 minutes
setInterval(updateDashboardCharts, 5 * 60 * 1000);

// Export all charts functionality
function exportAllCharts() {
    const charts = ['salesChart', 'orderStatusChart', 'categoryChart', 'monthlyRevenueChart'];
    charts.forEach((chartId, index) => {
        setTimeout(() => {
            exportChartAsImage(chartId, `dashboard-${chartId}.png`);
        }, index * 500); // Stagger exports
    });
}

// Add export button functionality
document.addEventListener('DOMContentLoaded', function() {
    addChartInteractions();
    
    // Add export button if needed
    const exportBtn = document.getElementById('export-charts-btn');
    if (exportBtn) {
        exportBtn.addEventListener('click', exportAllCharts);
    }
});

// Chart theme switching (if you want dark mode support)
function switchChartTheme(isDark) {
    const textColor = isDark ? '#e5e7eb' : '#6b7280';
    const gridColor = isDark ? '#374151' : '#e5e7eb';
    
    Chart.defaults.color = textColor;
    Chart.defaults.scale.grid.color = gridColor;
    
    // Update all existing charts
    Chart.helpers.each(Chart.instances, function(chart) {
        chart.options.scales.x.grid.color = gridColor;
        chart.options.scales.y.grid.color = gridColor;
        chart.options.scales.x.ticks.color = textColor;
        chart.options.scales.y.ticks.color = textColor;
        chart.update();
    });
}/
/ Toast notification system for product filters
function showToast(message, type = 'info', duration = 3000) {
    // Remove existing toasts
    const existingToasts = document.querySelectorAll('.toast-notification');
    existingToasts.forEach(toast => toast.remove());
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast-notification fixed top-4 right-4 z-50 px-6 py-3 rounded-lg shadow-lg transform transition-all duration-300 translate-x-full`;
    
    // Set toast style based on type
    switch (type) {
        case 'success':
            toast.classList.add('bg-green-500', 'text-white');
            break;
        case 'error':
            toast.classList.add('bg-red-500', 'text-white');
            break;
        case 'warning':
            toast.classList.add('bg-yellow-500', 'text-white');
            break;
        default:
            toast.classList.add('bg-blue-500', 'text-white');
    }
    
    // Add message
    toast.innerHTML = `
        <div class="flex items-center space-x-2">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-white hover:text-gray-200">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
            </button>
        </div>
    `;
    
    // Add to DOM
    document.body.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
        toast.classList.remove('translate-x-full');
    }, 100);
    
    // Auto remove
    setTimeout(() => {
        toast.classList.add('translate-x-full');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 300);
    }, duration);
}

// Product filter utilities
const ProductFilters = {
    // Initialize filter functionality
    init() {
        this.bindEvents();
        this.updateActiveFilters();
    },
    
    // Bind filter events
    bindEvents() {
        // Price range inputs
        const priceInputs = document.querySelectorAll('#min-price, #max-price');
        priceInputs.forEach(input => {
            input.addEventListener('input', this.debounce(() => {
                this.validatePriceRange();
            }, 500));
        });
        
        // Filter checkboxes and radios
        const filterInputs = document.querySelectorAll('.filter-input');
        filterInputs.forEach(input => {
            input.addEventListener('change', () => {
                this.updateActiveFilters();
            });
        });
    },
    
    // Validate price range inputs
    validatePriceRange() {
        const minPrice = document.getElementById('min-price');
        const maxPrice = document.getElementById('max-price');
        
        if (minPrice && maxPrice) {
            const min = parseFloat(minPrice.value) || 0;
            const max = parseFloat(maxPrice.value) || Infinity;
            
            if (min > max && max > 0) {
                maxPrice.value = min;
                showToast('সর্বোচ্চ দাম সর্বনিম্ন দামের চেয়ে কম হতে পারে না', 'warning');
            }
        }
    },
    
    // Update active filters display
    updateActiveFilters() {
        const activeFiltersContainer = document.getElementById('active-filters-list');
        const activeFiltersSection = document.getElementById('active-filters');
        
        if (!activeFiltersContainer || !activeFiltersSection) return;
        
        const activeFilters = [];
        
        // Check for active filters
        const checkedInputs = document.querySelectorAll('input:checked');
        checkedInputs.forEach(input => {
            if (input.name && input.value) {
                const label = input.closest('label')?.textContent?.trim() || input.value;
                activeFilters.push({
                    name: input.name,
                    value: input.value,
                    label: label
                });
            }
        });
        
        // Check price range
        const minPrice = document.getElementById('min-price')?.value;
        const maxPrice = document.getElementById('max-price')?.value;
        if (minPrice || maxPrice) {
            const priceLabel = `৳${minPrice || '0'} - ৳${maxPrice || '∞'}`;
            activeFilters.push({
                name: 'price',
                value: 'custom',
                label: priceLabel
            });
        }
        
        // Update display
        if (activeFilters.length > 0) {
            activeFiltersContainer.innerHTML = activeFilters.map(filter => `
                <span class="active-filter-tag">
                    ${filter.label}
                    <button onclick="ProductFilters.removeFilter('${filter.name}', '${filter.value}')" type="button">×</button>
                </span>
            `).join('');
            activeFiltersSection.classList.remove('hidden');
        } else {
            activeFiltersSection.classList.add('hidden');
        }
    },
    
    // Remove specific filter
    removeFilter(name, value) {
        if (name === 'price') {
            document.getElementById('min-price').value = '';
            document.getElementById('max-price').value = '';
        } else {
            const input = document.querySelector(`input[name="${name}"][value="${value}"]`);
            if (input) {
                input.checked = false;
            }
        }
        
        this.updateActiveFilters();
        // Auto-apply filters
        setTimeout(() => {
            const applyBtn = document.getElementById('apply-filters');
            if (applyBtn) applyBtn.click();
        }, 100);
    },
    
    // Debounce utility
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Initialize product filters when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.filter-sidebar') || document.querySelector('#filters-sidebar')) {
        ProductFilters.init();
    }
});

// Export for global use
window.ProductFilters = ProductFilters;
window.showToast = showToast;
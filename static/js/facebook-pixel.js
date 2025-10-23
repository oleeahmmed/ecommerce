// Facebook Pixel E-commerce Events
// This file handles Facebook Pixel tracking for e-commerce events

// Debug mode flag (will be set by Django template)
const FACEBOOK_PIXEL_DEBUG = window.FACEBOOK_PIXEL_DEBUG || false;

// Debug logging function
function debugLog(message, data = null) {
    if (FACEBOOK_PIXEL_DEBUG) {
        console.log('[Facebook Pixel]', message, data || '');
    }
}

// Check if Facebook Pixel is loaded
function isFacebookPixelLoaded() {
    const isLoaded = typeof fbq !== 'undefined';
    if (!isLoaded && FACEBOOK_PIXEL_DEBUG) {
        console.warn('[Facebook Pixel] fbq is not defined. Make sure Facebook Pixel is properly loaded.');
    }
    return isLoaded;
}

// Track ViewContent event
function trackViewContent(productData) {
    if (!isFacebookPixelLoaded()) return;

    const eventData = {
        content_type: 'product',
        content_ids: [productData.id],
        content_name: productData.name,
        content_category: productData.category,
        value: productData.price,
        currency: 'BDT'
    };

    debugLog('Tracking ViewContent', eventData);
    fbq('track', 'ViewContent', eventData);
}

// Track AddToCart event
function trackAddToCart(productData, quantity = 1) {
    if (!isFacebookPixelLoaded()) return;

    const eventData = {
        content_type: 'product',
        content_ids: [productData.id],
        content_name: productData.name,
        content_category: productData.category,
        value: productData.price * quantity,
        currency: 'BDT'
    };

    debugLog('Tracking AddToCart', eventData);
    fbq('track', 'AddToCart', eventData);
}

// Track InitiateCheckout event
function trackInitiateCheckout(cartData) {
    if (!isFacebookPixelLoaded()) return;

    const contentIds = cartData.items.map(item => item.product_id);
    const contents = cartData.items.map(item => ({
        id: item.product_id,
        quantity: item.quantity,
        item_price: item.price
    }));

    const eventData = {
        content_type: 'product',
        content_ids: contentIds,
        contents: contents,
        value: cartData.total,
        currency: 'BDT',
        num_items: cartData.items.length
    };

    debugLog('Tracking InitiateCheckout', eventData);
    fbq('track', 'InitiateCheckout', eventData);
}

// Track Purchase event
function trackPurchase(orderData) {
    if (!isFacebookPixelLoaded()) return;

    const contentIds = orderData.items.map(item => item.product_id);
    const contents = orderData.items.map(item => ({
        id: item.product_id,
        quantity: item.quantity,
        item_price: item.price
    }));

    const eventData = {
        content_type: 'product',
        content_ids: contentIds,
        contents: contents,
        value: orderData.total,
        currency: 'BDT',
        transaction_id: orderData.order_id
    };

    debugLog('Tracking Purchase', eventData);
    fbq('track', 'Purchase', eventData);
}

// Track Search event
function trackSearch(searchQuery, searchResults = null) {
    if (!isFacebookPixelLoaded()) return;

    const eventData = {
        search_string: searchQuery
    };

    if (searchResults) {
        eventData.content_ids = searchResults.map(product => product.id);
        eventData.contents = searchResults.map(product => ({
            id: product.id,
            quantity: 1,
            item_price: product.price
        }));
    }

    fbq('track', 'Search', eventData);
}

// Track Lead event (for newsletter signup, contact form, etc.)
function trackLead(leadData = {}) {
    if (!isFacebookPixelLoaded()) return;

    fbq('track', 'Lead', leadData);
}

// Track CompleteRegistration event
function trackCompleteRegistration() {
    if (!isFacebookPixelLoaded()) return;

    fbq('track', 'CompleteRegistration');
}

// Auto-track page-specific events
document.addEventListener('DOMContentLoaded', function () {
    if (!isFacebookPixelLoaded()) return;

    // Track product view on product detail pages
    const productData = window.productData;
    if (productData && window.location.pathname.includes('/product/')) {
        trackViewContent(productData);
    }

    // Track checkout initiation on checkout page
    const cartData = window.cartData;
    if (cartData && window.location.pathname.includes('/checkout/')) {
        trackInitiateCheckout(cartData);
    }

    // Track purchase on order confirmation page
    const orderData = window.orderData;
    if (orderData && window.location.pathname.includes('/order/confirmation/')) {
        trackPurchase(orderData);
    }

    // Track add to cart button clicks
    document.addEventListener('click', function (e) {
        if (e.target.matches('.add-to-cart-btn, .add-to-cart-btn *')) {
            const button = e.target.closest('.add-to-cart-btn');
            const productId = button.getAttribute('data-product-id');

            if (productId && window.productData) {
                const quantity = document.querySelector('#quantity')?.value || 1;
                trackAddToCart(window.productData, parseInt(quantity));
            }
        }
    });

    // Track search events
    const searchForms = document.querySelectorAll('form[action*="search"], #searchInput');
    searchForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const searchInput = form.querySelector('input[type="text"], input[type="search"]') || form;
            const searchQuery = searchInput.value.trim();

            if (searchQuery) {
                trackSearch(searchQuery);
            }
        });
    });

    // Track newsletter signup
    const newsletterForms = document.querySelectorAll('form[action*="newsletter"], .newsletter-form');
    newsletterForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            trackLead({ content_name: 'Newsletter Signup' });
        });
    });

    // Track contact form submission
    const contactForms = document.querySelectorAll('form[action*="contact"], .contact-form');
    contactForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            trackLead({ content_name: 'Contact Form' });
        });
    });
});

// Export functions for global use
window.FacebookPixelTracker = {
    trackViewContent,
    trackAddToCart,
    trackInitiateCheckout,
    trackPurchase,
    trackSearch,
    trackLead,
    trackCompleteRegistration
};
// main.js - Complete Working JavaScript for কাঁচাবাজার
document.addEventListener('DOMContentLoaded', function() {
    console.log('কাঁচাবাজার শুরু হচ্ছে...');
    
    // Initialize all functionality
    initializeCartData();
    setupEventListeners();
    setupCartFunctionality();
    setupModalFunctionality();
    setupSearchFunctionality();
    
    console.log('কাঁচাবাজার সফলভাবে শুরু হয়েছে!');
});

// Global cart state
let cartState = {
    itemsCount: 0,
    totalPrice: 0
};

function setupEventListeners() {
    console.log('ইভেন্ট লিসেনার সেটআপ হচ্ছে...');
    
    // Cart sidebar functionality
    const cartSidebar = document.getElementById('cartSidebar');
    const cartOverlay = document.getElementById('cartOverlay');
    const cartButton = document.getElementById('cartButton');
    const floatingCartBtn = document.querySelector('.floating-cart-btn');
    const footerCartBtn = document.querySelector('.footer-cart-btn');
    const closeCart = document.getElementById('closeCart');
    
    // Search functionality
    const searchPopup = document.getElementById('searchPopup');
    const searchOverlay = document.getElementById('searchOverlay');
    const mobileSearchButton = document.getElementById('mobileSearchButton');
    const desktopSearchButton = document.getElementById('desktopSearchButton');
    const closeSearch = document.getElementById('closeSearch');
    
    // Mobile menu functionality
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileOverlay = document.getElementById('mobileOverlay');
    const mobileMenuButton = document.getElementById('mobileMenuButton');
    const mobileMenuButtonFooter = document.getElementById('mobileMenuButtonFooter');
    const closeMobileMenu = document.getElementById('closeMobileMenu');

    // Cart open/close functions
    function openCart() {
        console.log('কার্ট সাইডবার খোলা হচ্ছে...');
        if (cartSidebar) cartSidebar.classList.add('active');
        if (cartOverlay) cartOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeCartSidebar() {
        console.log('কার্ট সাইডবার বন্ধ হচ্ছে...');
        if (cartSidebar) cartSidebar.classList.remove('active');
        if (cartOverlay) cartOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    // Event listeners for cart
    if (cartButton) {
        cartButton.addEventListener('click', openCart);
        console.log('কার্ট বাটন লিসেনার যোগ করা হয়েছে');
    }
    
    if (floatingCartBtn) {
        floatingCartBtn.addEventListener('click', openCart);
        console.log('ফ্লোয়াটিং কার্ট বাটন লিসেনার যোগ করা হয়েছে');
    }
    
    if (footerCartBtn) {
        footerCartBtn.addEventListener('click', openCart);
        console.log('ফুটার কার্ট বাটন লিসেনার যোগ করা হয়েছে');
    }
    
    if (closeCart) {
        closeCart.addEventListener('click', closeCartSidebar);
    }
    
    if (cartOverlay) {
        cartOverlay.addEventListener('click', closeCartSidebar);
    }

    // Search functionality
    function openSearch() {
        if (searchPopup) searchPopup.classList.add('active');
        if (searchOverlay) searchOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        const searchInput = document.getElementById('searchInput');
        if (searchInput) searchInput.focus();
    }

    function closeSearchPopup() {
        if (searchPopup) searchPopup.classList.remove('active');
        if (searchOverlay) searchOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (mobileSearchButton) {
        mobileSearchButton.addEventListener('click', openSearch);
    }
    
    if (desktopSearchButton) {
        desktopSearchButton.addEventListener('click', openSearch);
    }
    
    if (closeSearch) {
        closeSearch.addEventListener('click', closeSearchPopup);
    }
    
    if (searchOverlay) {
        searchOverlay.addEventListener('click', closeSearchPopup);
    }

    // Mobile menu functionality
    function openMobileMenu() {
        if (mobileMenu) mobileMenu.classList.add('active');
        if (mobileOverlay) mobileOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeMobileMenuFunc() {
        if (mobileMenu) mobileMenu.classList.remove('active');
        if (mobileOverlay) mobileOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', openMobileMenu);
    }
    
    if (mobileMenuButtonFooter) {
        mobileMenuButtonFooter.addEventListener('click', openMobileMenu);
    }
    
    if (closeMobileMenu) {
        closeMobileMenu.addEventListener('click', closeMobileMenuFunc);
    }
    
    if (mobileOverlay) {
        mobileOverlay.addEventListener('click', closeMobileMenuFunc);
    }

    console.log('সমস্ত ইভেন্ট লিসেনার সেটআপ সম্পূর্ণ');
}

function setupCartFunctionality() {
    console.log('কার্ট ফাংশনালিটি সেটআপ হচ্ছে...');
    
    // Add to cart functionality
    document.addEventListener('click', function(e) {
        // Add to cart from product grid and detail pages
        if (e.target.closest('.add-to-cart-btn')) {
            e.preventDefault();
            const button = e.target.closest('.add-to-cart-btn');
            const productId = button.getAttribute('data-product-id');
            
            if (!productId) {
                console.error('Add to cart বাটনে পণ্য ID পাওয়া যায়নি');
                showToast('ত্রুটি: পণ্য ID পাওয়া যায়নি', 'error');
                return;
            }
            
            let quantity = 1;
            
            // Try to find quantity from nearby elements
            const card = button.closest('.bg-white'); // Product card
            if (card) {
                const quantitySelect = card.querySelector('select[name="quantity"]');
                if (quantitySelect) {
                    quantity = parseInt(quantitySelect.value);
                }
            }
            
            // Check if we're on product detail page
            const detailQuantity = document.getElementById('quantity');
            if (detailQuantity) {
                quantity = parseInt(detailQuantity.value);
            }
            
            console.log(`পণ্য ${productId} কার্টে যোগ করা হচ্ছে, পরিমাণ: ${quantity}`);
            addToCart(productId, quantity);
        }
        
        // Buy now functionality from product grid
        if (e.target.closest('.buy-now-btn')) {
            e.preventDefault();
            const button = e.target.closest('.buy-now-btn');
            const productId = button.getAttribute('data-product-id');
            
            if (!productId) {
                console.error('Buy now বাটনে পণ্য ID পাওয়া যায়নি');
                showToast('ত্রুটি: পণ্য ID পাওয়া যায়নি', 'error');
                return;
            }
            
            let quantity = 1;
            
            // Try to find quantity from nearby elements in product grid
            const card = button.closest('.product-card');
            if (card) {
                const quantitySelect = card.querySelector('select[name="quantity"]');
                if (quantitySelect) {
                    quantity = parseInt(quantitySelect.value);
                }
            }
            
            // Check if we're on product detail page
            const detailQuantity = document.getElementById('quantity');
            if (detailQuantity) {
                quantity = parseInt(detailQuantity.value);
            }
            
            console.log(`এখনই কিনুন - পণ্য: ${productId}, পরিমাণ: ${quantity}`);
            buyNow(productId, quantity);
        }
        
        // Quick view add to cart
        if (e.target.closest('.quick-view-add-to-cart')) {
            e.preventDefault();
            const button = e.target.closest('.quick-view-add-to-cart');
            const productId = button.getAttribute('data-product-id');
            const quantityInput = document.getElementById('quickViewQuantity');
            const quantity = quantityInput ? parseInt(quantityInput.value) : 1;
            
            console.log(`কুইক ভিউ - পণ্য ${productId} কার্টে যোগ করা হচ্ছে`);
            addToCart(productId, quantity);
            
            // Close quick view modal after adding to cart
            const quickViewModal = document.getElementById('quickViewModal');
            if (quickViewModal) {
                quickViewModal.classList.remove('active');
            }
        }
        
        // Buy now functionality
        if (e.target.closest('.buy-now-btn')) {
            e.preventDefault();
            const button = e.target.closest('.buy-now-btn');
            const productId = button.getAttribute('data-product-id');
            
            let quantity = 1;
            const detailQuantity = document.getElementById('quantity');
            if (detailQuantity) {
                quantity = parseInt(detailQuantity.value);
            }
            
            console.log(`এখনই কিনুন - পণ্য ${productId}`);
            buyNow(productId, quantity);
        }
        
        // Quick view buy now
        if (e.target.closest('.quick-view-buy-now')) {
            e.preventDefault();
            const button = e.target.closest('.quick-view-buy-now');
            const productId = button.getAttribute('data-product-id');
            const quantityInput = document.getElementById('quickViewQuantity');
            const quantity = quantityInput ? parseInt(quantityInput.value) : 1;
            
            console.log(`কুইক ভিউ এখনই কিনুন - পণ্য ${productId}`);
            buyNow(productId, quantity);
        }
    });

    // Cart item quantity management - FIXED SELECTORS
    document.addEventListener('click', function(e) {
        // Increase quantity in cart
        if (e.target.closest('.increase-quantity')) {
            const button = e.target.closest('.increase-quantity');
            const itemId = button.getAttribute('data-item-id');
            if (itemId) {
                const quantityInput = document.querySelector(`.quantity-input[data-item-id="${itemId}"]`);
                if (quantityInput) {
                    const currentQuantity = parseInt(quantityInput.value);
                    const newQuantity = currentQuantity + 1;
                    quantityInput.value = newQuantity;
                    updateCartItem(itemId, newQuantity);
                }
            }
        }
        
        // Decrease quantity in cart
        if (e.target.closest('.decrease-quantity')) {
            const button = e.target.closest('.decrease-quantity');
            const itemId = button.getAttribute('data-item-id');
            if (itemId) {
                const quantityInput = document.querySelector(`.quantity-input[data-item-id="${itemId}"]`);
                if (quantityInput) {
                    const currentQuantity = parseInt(quantityInput.value);
                    if (currentQuantity > 1) {
                        const newQuantity = currentQuantity - 1;
                        quantityInput.value = newQuantity;
                        updateCartItem(itemId, newQuantity);
                    } else {
                        removeFromCart(itemId);
                    }
                }
            }
        }
        
        // Remove item from cart - FIXED SELECTOR
        if (e.target.closest('.remove-cart-item')) {
            const button = e.target.closest('.remove-cart-item');
            const itemId = button.getAttribute('data-item-id');
            if (itemId) {
                removeFromCart(itemId);
            }
        }
    });

    // Quantity input change
    document.addEventListener('change', function(e) {
        if (e.target.classList.contains('quantity-input')) {
            const input = e.target;
            const itemId = input.getAttribute('data-item-id');
            const quantity = parseInt(input.value);
            
            if (itemId && quantity > 0) {
                updateCartItem(itemId, quantity);
            } else if (itemId) {
                removeFromCart(itemId);
            }
        }
    });

    console.log('কার্ট ফাংশনালিটি সেটআপ সম্পূর্ণ');
}

function setupModalFunctionality() {
    console.log('মোডাল ফাংশনালিটি সেটআপ হচ্ছে...');
    
    // Quick view functionality
    document.addEventListener('click', function(e) {
        if (e.target.closest('.quick-view-btn')) {
            e.preventDefault();
            const button = e.target.closest('.quick-view-btn');
            const productId = button.getAttribute('data-product-id');
            
            if (productId) {
                console.log(`পণ্য ${productId} এর কুইক ভিউ খোলা হচ্ছে`);
                openQuickView(productId);
            }
        }
    });

    // Modal close functionality
    document.addEventListener('click', function(e) {
        // Close modals when clicking close button
        if (e.target.classList.contains('close-modal') || e.target.closest('.close-modal')) {
            const modal = e.target.closest('.modal');
            if (modal) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            }
        }
        
        // Close modals when clicking outside
        if (e.target.classList.contains('modal')) {
            e.target.classList.remove('active');
            document.body.style.overflow = '';
        }
    });

    console.log('মোডাল ফাংশনালিটি সেটআপ সম্পূর্ণ');
}

function setupSearchFunctionality() {
    console.log('সার্চ ফাংশনালিটি সেটআপ হচ্ছে...');
    
    // Search functionality
    const searchInput = document.getElementById('searchInput');
    const mainSearchInput = document.getElementById('mainSearchInput');
    
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch(this.value);
            }
        });
    }
    
    if (mainSearchInput) {
        mainSearchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch(this.value);
            }
        });
    }
    
    // Popular search tags
    document.querySelectorAll('.search-tag').forEach(tag => {
        tag.addEventListener('click', function() {
            const query = this.getAttribute('data-query') || this.textContent;
            performSearch(query);
        });
    });

    console.log('সার্চ ফাংশনালিটি সেটআপ সম্পূর্ণ');
}

// API Functions
function addToCart(productId, quantity = 1) {
    console.log(`API: কার্টে যোগ করা হচ্ছে - পণ্য: ${productId}, পরিমাণ: ${quantity}`);
    
    showLoadingState(true);
    
    fetch('/cart/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: parseInt(quantity)
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('কার্টে যোগ করার রেসপন্স:', data);
        if (data.success) {
            updateCartUI(data);
            showToast('পণ্য সফলভাবে কার্টে যোগ করা হয়েছে!', 'success');
            // Open cart sidebar when item is added
            openCartSidebar();
        } else {
            showToast(data.message || 'পণ্য কার্টে যোগ করতে ব্যর্থ হয়েছে', 'error');
        }
    })
    .catch(error => {
        console.error('কার্টে যোগ করার সময় ত্রুটি:', error);
        showToast('পণ্য কার্টে যোগ করতে সমস্যা হয়েছে। আবার চেষ্টা করুন।', 'error');
    })
    .finally(() => {
        showLoadingState(false);
    });
}

function updateCartItem(itemId, quantity) {
    console.log(`API: কার্ট আইটেম আপডেট করা হচ্ছে - আইটেম: ${itemId}, পরিমাণ: ${quantity}`);
    
    showLoadingState(true);
    
    fetch('/cart/update/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            item_id: itemId,
            quantity: parseInt(quantity)
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('কার্ট আপডেট রেসপন্স:', data);
        if (data.success) {
            updateCartUI(data);
            showToast('কার্ট সফলভাবে আপডেট করা হয়েছে!', 'success');
        } else {
            showToast(data.message || 'কার্ট আপডেট করতে ব্যর্থ হয়েছে', 'error');
        }
    })
    .catch(error => {
        console.error('কার্ট আপডেট করার সময় ত্রুটি:', error);
        showToast('কার্ট আপডেট করতে সমস্যা হয়েছে। আবার চেষ্টা করুন।', 'error');
    })
    .finally(() => {
        showLoadingState(false);
    });
}

function removeFromCart(itemId) {
    console.log(`API: কার্ট থেকে সরানো হচ্ছে - আইটেম: ${itemId}`);
    
    showLoadingState(true);
    
    fetch('/cart/remove/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            item_id: itemId
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('কার্ট থেকে সরানোর রেসপন্স:', data);
        if (data.success) {
            updateCartUI(data);
            showToast('আইটেম কার্ট থেকে সরানো হয়েছে', 'success');
        } else {
            showToast(data.message || 'আইটেম সরাতে ব্যর্থ হয়েছে', 'error');
        }
    })
    .catch(error => {
        console.error('কার্ট থেকে সরানোর সময় ত্রুটি:', error);
        showToast('আইটেম কার্ট থেকে সরাতে সমস্যা হয়েছে। আবার চেষ্টা করুন।', 'error');
    })
    .finally(() => {
        showLoadingState(false);
    });
}

function buyNow(productId, quantity = 1) {
    console.log(`এখনই কিনুন - পণ্য: ${productId}, পরিমাণ: ${quantity}`);
    
    // First add to cart, then redirect to checkout
    addToCart(productId, quantity);
    
    // Redirect to checkout after a short delay to allow cart update
    setTimeout(() => {
        window.location.href = '/checkout/';
    }, 1500);
}

function openQuickView(productId) {
    console.log(`পণ্যের কুইক ভিউ খোলা হচ্ছে: ${productId}`);
    
    const modal = document.getElementById('quickViewModal');
    const content = document.getElementById('quickViewContent');
    
    if (!modal || !content) {
        console.error('কুইক ভিউ মোডাল বা কন্টেন্ট পাওয়া যায়নি');
        showToast('কুইক ভিউ ফিচারটি বর্তমানে unavailable', 'error');
        return;
    }
    
    // Show loading state
    content.innerHTML = `
        <div class="flex items-center justify-center py-12">
            <div class="loading-spinner"></div>
            <span class="ml-2">পণ্যের বিস্তারিত লোড হচ্ছে...</span>
        </div>
    `;
    
    modal.classList.add('active');
    
    // Fetch quick view data
    fetch(`/product/quick-view/${productId}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(html => {
            content.innerHTML = html;
            console.log('কুইক ভিউ কন্টেন্ট সফলভাবে লোড হয়েছে');
        })
        .catch(error => {
            console.error('কুইক ভিউ লোড করার সময় ত্রুটি:', error);
            content.innerHTML = `
                <div class="text-center py-12">
                    <svg class="w-12 h-12 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/>
                    </svg>
                    <p class="text-red-500">পণ্যের বিস্তারিত লোড করতে সমস্যা হয়েছে। আবার চেষ্টা করুন।</p>
                    <button class="mt-4 px-4 py-2 bg-primary text-white rounded hover:bg-primary-dark transition close-modal">
                        বন্ধ করুন
                    </button>
                </div>
            `;
        });
}

// UI Update Functions
function updateCartUI(data) {
    console.log('কার্ট UI আপডেট করা হচ্ছে:', data);
    
    // Update global cart state
    cartState.itemsCount = data.cart_items_count || 0;
    cartState.totalPrice = data.cart_total || 0;
    
    // Update cart items count badge
    const cartBadges = document.querySelectorAll('.cart-badge');
    cartBadges.forEach(badge => {
        badge.textContent = cartState.itemsCount;
        badge.style.display = cartState.itemsCount > 0 ? 'flex' : 'none';
    });
    
    // Update cart count text
    const cartCountElements = document.querySelectorAll('#cartCount');
    cartCountElements.forEach(element => {
        element.textContent = cartState.itemsCount;
        element.style.display = cartState.itemsCount > 0 ? 'flex' : 'none';
    });
    
    // Update cart total price
    const cartTotalElements = document.querySelectorAll('#cartTotal, .cart-total-text');
    cartTotalElements.forEach(element => {
        element.textContent = `৳${parseFloat(cartState.totalPrice).toFixed(2)}`;
    });
    
    // Update cart items text
    const cartItemsTextElements = document.querySelectorAll('.cart-items-text');
    cartItemsTextElements.forEach(element => {
        element.textContent = `${cartState.itemsCount} ${cartState.itemsCount === 1 ? 'আইটেম' : 'আইটেম'}`;
    });
    
    // Update cart items HTML if provided
    if (data.cart_items_html && document.getElementById('cartItems')) {
        document.getElementById('cartItems').innerHTML = data.cart_items_html;
    }
    
    console.log('কার্ট UI সফলভাবে আপডেট হয়েছে');
}

function openCartSidebar() {
    console.log('প্রোগ্রাম্যাটিকভাবে কার্ট সাইডবার খোলা হচ্ছে...');
    const cartSidebar = document.getElementById('cartSidebar');
    const cartOverlay = document.getElementById('cartOverlay');
    
    if (cartSidebar && cartOverlay) {
        cartSidebar.classList.add('active');
        cartOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

// Utility Functions
function getCSRFToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfToken) {
        return csrfToken.value;
    }
    
    // Fallback: check cookies
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showToast(message, type = 'success') {
    console.log(`টোস্ট দেখানো হচ্ছে: ${message} (${type})`);
    
    // Remove existing toasts
    const existingToasts = document.querySelectorAll('.toast');
    existingToasts.forEach(toast => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    });
    
    // Create new toast
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: ${type === 'error' ? '#ef4444' : '#10b981'};
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 2000;
        animation: slideIn 0.3s ease;
    `;
    
    // Add CSS animation if not exists
    if (!document.querySelector('#toast-animation')) {
        const style = document.createElement('style');
        style.id = 'toast-animation';
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(400px); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(toast);
    
    // Remove toast after 3 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 3000);
}

function showLoadingState(show) {
    // You can implement a global loading indicator here
    if (show) {
        // Show loading state
        console.log('লোডিং স্টেট দেখানো হচ্ছে...');
    } else {
        // Hide loading state
        console.log('লোডিং স্টেট লুকানো হচ্ছে...');
    }
}

function performSearch(query) {
    if (query && query.trim()) {
        console.log(`সার্চ করা হচ্ছে: ${query}`);
        
        // Track search query
        fetch('/track-search/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({
                query: query.trim()
            })
        }).catch(error => {
            console.log('Search tracking failed:', error);
        });
        
        window.location.href = `/products/?search=${encodeURIComponent(query.trim())}`;
    }
}

// Initialize cart data on page load
function initializeCartData() {
    console.log('কার্ট ডেটা ইনিশিয়ালাইজ করা হচ্ছে...');
    
    fetch('/cart/data/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('কার্ট ডেটা লোড হয়েছে:', data);
            updateCartUI(data);
        })
        .catch(error => {
            console.error('কার্ট ডেটা ফেচ করার সময় ত্রুটি:', error);
            // Set default cart state
            updateCartUI({
                cart_items_count: 0,
                cart_total: 0
            });
        });
}
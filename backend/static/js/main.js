// Main JavaScript for Home Page

document.addEventListener('DOMContentLoaded', function() {
    // Animate numbers
    animateNumbers();
    
    // Smooth scroll for navigation links
    setupSmoothScroll();
    
    // Fetch and display stats
    fetchStats();
    
    // Add scroll animations
    setupScrollAnimations();
});

// Animate numbers with counting effect
function animateNumbers() {
    const totalProductsEl = document.getElementById('totalProducts');
    const totalImagesEl = document.getElementById('totalImages');
    
    if (totalProductsEl) {
        animateValue(totalProductsEl, 0, 0, 1000);
    }
    if (totalImagesEl) {
        animateValue(totalImagesEl, 0, 0, 1000);
    }
}

function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = Math.floor(progress * (end - start) + start);
        element.textContent = value;
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Fetch stats from API
async function fetchStats() {
    try {
        // Fetch products count
        const productsResponse = await fetch('/api/v1/products');
        if (productsResponse.ok) {
            const products = await productsResponse.json();
            const totalProductsEl = document.getElementById('totalProducts');
            if (totalProductsEl) {
                animateValue(totalProductsEl, 0, products.length || 0, 1500);
            }
        }
        
        // Fetch images count
        const imagesResponse = await fetch('/api/v1/images?limit=1000');
        if (imagesResponse.ok) {
            const images = await imagesResponse.json();
            const totalImagesEl = document.getElementById('totalImages');
            if (totalImagesEl) {
                animateValue(totalImagesEl, 0, images.length || 0, 1500);
            }
        }
    } catch (error) {
        console.log('Could not fetch stats:', error);
        // Set default values if API is not available
        const totalProductsEl = document.getElementById('totalProducts');
        const totalImagesEl = document.getElementById('totalImages');
        if (totalProductsEl) totalProductsEl.textContent = '0';
        if (totalImagesEl) totalImagesEl.textContent = '0';
    }
}

// Setup smooth scroll for anchor links
function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

// Setup scroll animations
function setupScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe feature cards and analytics cards
    document.querySelectorAll('.feature-card, .analytics-card, .endpoint-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

// Add active state to navigation on scroll
window.addEventListener('scroll', function() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-menu a[href^="#"]');
    
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (window.pageYOffset >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// Fix button clicks
document.addEventListener('click', function(e) {
    // Handle buttons with href
    if (e.target.closest('.btn')) {
        const btn = e.target.closest('.btn');
        const href = btn.getAttribute('href');
        if (href && href.startsWith('#')) {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    }
});


// Dashboard JavaScript

const API_BASE = '/api/v1';

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupNavigation();
    setupUpload();
    setupProductForm();
    loadProducts();
    loadImages();
    loadAnalytics();
});

// Navigation
function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item[data-section]');
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const section = this.getAttribute('data-section');
            switchSection(section);
            
            // Update active nav
            navItems.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

function switchSection(section) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(sec => {
        sec.classList.remove('active');
    });
    
    // Show selected section
    const targetSection = document.getElementById(`${section}-section`);
    if (targetSection) {
        targetSection.classList.add('active');
    }
    
    // Update page title
    const titles = {
        'products': 'مدیریت محصولات',
        'images': 'مدیریت تصاویر',
        'upload': 'آپلود تصویر',
        'analytics': 'تحلیل‌ها'
    };
    document.getElementById('page-title').textContent = titles[section] || 'پنل مدیریت';
}

// Products Management
async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE}/products`);
        const products = await response.json();
        displayProducts(products);
    } catch (error) {
        showToast('خطا در بارگذاری محصولات', 'error');
        console.error('Error loading products:', error);
    }
}

function displayProducts(products) {
    const tbody = document.getElementById('products-table-body');
    
    if (products.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="loading">محصولی یافت نشد</td></tr>';
        return;
    }
    
    tbody.innerHTML = products.map(product => `
        <tr>
            <td>${product.id}</td>
            <td>${product.name}</td>
            <td>${product.category || '-'}</td>
            <td>${new Date().toLocaleDateString('fa-IR')}</td>
            <td>
                <button class="btn btn-danger" onclick="deleteProduct(${product.id})">
                    <i class="fas fa-trash"></i>
                    حذف
                </button>
            </td>
        </tr>
    `).join('');
}

document.getElementById('add-product-btn').addEventListener('click', function() {
    document.getElementById('product-form').reset();
    document.getElementById('product-id').value = '';
    document.getElementById('modal-title').textContent = 'افزودن محصول جدید';
    document.getElementById('product-modal').classList.add('active');
});

function setupProductForm() {
    const form = document.getElementById('product-form');
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const productId = document.getElementById('product-id').value;
        const name = document.getElementById('product-name').value;
        const category = document.getElementById('product-category').value;
        
        try {
            // Validate name
            if (!name || !name.trim()) {
                showToast('نام محصول الزامی است', 'error');
                return;
            }
            
            const url = productId ? `${API_BASE}/products/${productId}` : `${API_BASE}/products`;
            const method = productId ? 'PUT' : 'POST';
            
            const payload = {
                name: name.trim(),
                category: category && category.trim() ? category.trim() : null
            };
            
            console.log('Sending request to:', url);
            console.log('Payload:', payload);
            
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify(payload)
            });
            
            console.log('Response status:', response.status);
            const responseData = await response.json();
            console.log('Response data:', responseData);
            
            if (response.ok) {
                showToast('محصول با موفقیت ذخیره شد', 'success');
                document.getElementById('product-modal').classList.remove('active');
                form.reset();
                document.getElementById('product-id').value = '';
                loadProducts();
            } else {
                let errorMessage = 'خطا در ذخیره محصول';
                
                if (responseData.message) {
                    errorMessage = responseData.message;
                } else if (responseData.error) {
                    errorMessage = responseData.error;
                } else if (responseData.details) {
                    // Handle validation errors
                    const errors = Object.values(responseData.details).flat();
                    errorMessage = errors.join(', ');
                } else if (responseData.name && Array.isArray(responseData.name)) {
                    errorMessage = responseData.name[0];
                } else if (typeof responseData === 'string') {
                    errorMessage = responseData;
                }
                
                showToast(errorMessage, 'error');
                console.error('Error details:', responseData);
            }
        } catch (error) {
            showToast('خطا در ارتباط با سرور', 'error');
            console.error('Error saving product:', error);
        }
    });
    
    document.getElementById('close-modal').addEventListener('click', function() {
        document.getElementById('product-modal').classList.remove('active');
    });
    
    document.getElementById('cancel-btn').addEventListener('click', function() {
        document.getElementById('product-modal').classList.remove('active');
    });
}

async function deleteProduct(id) {
    if (!confirm('آیا از حذف این محصول اطمینان دارید؟')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/products/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showToast('محصول با موفقیت حذف شد', 'success');
            loadProducts();
        } else {
            showToast('خطا در حذف محصول', 'error');
        }
    } catch (error) {
        showToast('خطا در ارتباط با سرور', 'error');
        console.error('Error deleting product:', error);
    }
}

// Images Management
async function loadImages() {
    try {
        const response = await fetch(`${API_BASE}/images?limit=50`);
        const images = await response.json();
        displayImages(images);
    } catch (error) {
        showToast('خطا در بارگذاری تصاویر', 'error');
        console.error('Error loading images:', error);
    }
}

function displayImages(images) {
    const grid = document.getElementById('images-grid');
    
    if (images.length === 0) {
        grid.innerHTML = '<div class="loading">تصویری یافت نشد</div>';
        return;
    }
    
    grid.innerHTML = images.map(image => {
        // Handle path - could be relative or absolute
        let imageUrl = image.path;
        if (!imageUrl.startsWith('http') && !imageUrl.startsWith('/')) {
            // Relative path - make it absolute for media
            imageUrl = imageUrl.replace(/\\/g, '/');
            if (!imageUrl.startsWith('storage/')) {
                imageUrl = `storage/images/${imageUrl.split('/').pop()}`;
            }
            imageUrl = `/media/${imageUrl}`;
        } else if (imageUrl.includes('storage')) {
            imageUrl = `/media/${imageUrl.replace(/\\/g, '/')}`;
        }
        
        return `
        <div class="image-card">
            <img src="${imageUrl}" alt="Image ${image.id}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'300\' height=\'200\'%3E%3Crect fill=\'%231e293b\' width=\'300\' height=\'200\'/%3E%3Ctext x=\'50%25\' y=\'50%25\' text-anchor=\'middle\' dy=\'.3em\' fill=\'%23cbd5e1\' font-family=\'Arial\'%3Eتصویر%3C/text%3E%3C/svg%3E'">
            <div class="image-card-body">
                <h3>تصویر ${image.id}</h3>
                <p>${new Date(image.date).toLocaleDateString('fa-IR')}</p>
            </div>
        </div>
    `;
    }).join('');
}

// Upload
function setupUpload() {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('image-input');
    
    uploadArea.addEventListener('click', () => fileInput.click());
    
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            uploadImage(e.target.files[0]);
        }
    });
    
    // Drag and drop
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', function() {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        if (e.dataTransfer.files.length > 0) {
            uploadImage(e.dataTransfer.files[0]);
        }
    });
}

async function uploadImage(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const progressDiv = document.getElementById('upload-progress');
    const resultDiv = document.getElementById('upload-result');
    const progressFill = document.getElementById('progress-fill');
    
    progressDiv.style.display = 'block';
    resultDiv.style.display = 'none';
    progressFill.style.width = '0%';
    
    try {
        const xhr = new XMLHttpRequest();
        
        xhr.upload.addEventListener('progress', function(e) {
            if (e.lengthComputable) {
                const percent = (e.loaded / e.total) * 100;
                progressFill.style.width = percent + '%';
            }
        });
        
        xhr.addEventListener('load', function() {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                displayUploadResult(response);
                progressDiv.style.display = 'none';
                resultDiv.style.display = 'block';
                showToast('تصویر با موفقیت آپلود شد', 'success');
                loadImages();
                loadProducts();
            } else {
                showToast('خطا در آپلود تصویر', 'error');
                progressDiv.style.display = 'none';
            }
        });
        
        xhr.addEventListener('error', function() {
            showToast('خطا در ارتباط با سرور', 'error');
            progressDiv.style.display = 'none';
        });
        
        xhr.open('POST', `${API_BASE}/images/upload`);
        xhr.send(formData);
        
    } catch (error) {
        showToast('خطا در آپلود تصویر', 'error');
        progressDiv.style.display = 'none';
        console.error('Error uploading image:', error);
    }
}

function displayUploadResult(result) {
    const resultsDiv = document.getElementById('detection-results');
    
    const numModels = result.detections ? result.detections.length : 0;
    
    resultsDiv.innerHTML = `
        <div class="detection-item">
            <span>کل محصولات شناسایی شده:</span>
            <span class="badge">${result.total_products}</span>
        </div>
        <div class="detection-item">
            <span>تعداد مدل‌های مختلف:</span>
            <span class="badge">${numModels} مدل</span>
        </div>
        <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #e2e8f0;">
            <h4 style="margin-bottom: 15px; color: #1e293b;">جزئیات محصولات:</h4>
            ${result.detections.map(det => `
                <div class="detection-item" style="margin-bottom: 10px;">
                    <span>${det.product_name}</span>
                    <span class="badge">${det.count} عدد (${(det.confidence * 100).toFixed(1)}%)</span>
                </div>
            `).join('')}
        </div>
    `;
}

// Analytics
async function loadAnalytics() {
    try {
        const response = await fetch(`${API_BASE}/analytics/weekly?days=7`);
        const data = await response.json();
        displayAnalytics(data);
    } catch (error) {
        showToast('خطا در بارگذاری تحلیل‌ها', 'error');
        console.error('Error loading analytics:', error);
    }
}

function displayAnalytics(data) {
    const cardsDiv = document.getElementById('analytics-cards');
    
    if (data.products && data.products.length > 0) {
        cardsDiv.innerHTML = data.products.map(product => `
            <div class="analytics-card">
                <h3>${product.product_name}</h3>
                <p>متوسط تقاضای روزانه: <strong>${product.average_daily_demand.toFixed(1)}</strong></p>
                <p>نرخ رشد: <strong>${product.growth_rate.toFixed(2)}%</strong></p>
                <p>ثبات تقاضا: <strong>${product.demand_consistency.toFixed(2)}%</strong></p>
                <p>تعداد کل: <strong>${product.total_count}</strong></p>
            </div>
        `).join('');
    } else {
        cardsDiv.innerHTML = '<div class="loading">داده‌ای برای نمایش وجود ندارد</div>';
    }
}

// Toast Notifications
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icon = type === 'success' ? 'fa-check-circle' : 
                 type === 'error' ? 'fa-exclamation-circle' : 
                 'fa-info-circle';
    
    toast.innerHTML = `
        <i class="fas ${icon}"></i>
        <span>${message}</span>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease-out reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Refresh button
document.getElementById('refresh-btn').addEventListener('click', function() {
    const activeSection = document.querySelector('.content-section.active');
    if (activeSection.id === 'products-section') {
        loadProducts();
    } else if (activeSection.id === 'images-section') {
        loadImages();
    } else if (activeSection.id === 'analytics-section') {
        loadAnalytics();
    }
});


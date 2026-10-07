// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 2
    }).format(amount);
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function showSpinner() {
    const spinner = document.createElement('div');
    spinner.id = 'loading-spinner';
    spinner.innerHTML = `
        <div class="spinner"></div>
        <p class="loading-dots">Analyzing your transactions</p>
    `;
    document.body.appendChild(spinner);
}

function hideSpinner() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.remove();
    }
}

// File Upload Handler
function initFileUpload() {
    const uploadBox = document.getElementById('fileUploadBox');
    const fileInput = document.getElementById('pdfFile');
    const uploadForm = document.getElementById('uploadForm');
    const fileName = document.getElementById('fileName');
    
    if (!uploadBox || !fileInput) return;
    
    console.log('initFileUpload called'); // Debug log
    
    // Click to select file
    uploadBox.addEventListener('click', () => {
        fileInput.click();
    });
    
    // File selected
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            fileName.textContent = `Selected: ${file.name}`;
            uploadBox.classList.add('file-selected');
        }
    });
    
    // Drag and drop
    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.classList.add('dragover');
    });
    
    uploadBox.addEventListener('dragleave', () => {
        uploadBox.classList.remove('dragover');
    });
    
    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            fileName.textContent = `Selected: ${files[0].name}`;
            uploadBox.classList.add('file-selected');
        }
    });
    
    // Form submission
    if (uploadForm) {
        let isSubmitting = false; // Prevent double submission
        
        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            console.log('Form submit triggered, isSubmitting:', isSubmitting); // Debug log
            
            // Prevent double submission
            if (isSubmitting) {
                console.log('Already submitting, blocking duplicate'); // Debug log
                return;
            }
            
            const formData = new FormData(uploadForm);
            const file = fileInput.files[0];
            
            if (!file) {
                showAlert('Please select a PDF file', 'error');
                return;
            }
            
            isSubmitting = true;
            
            // Disable submit button
            const submitBtn = uploadForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = 'Analyzing...';
            
            showSpinner();
            
            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                hideSpinner();
                
                if (result.success) {
                    window.location.href = result.redirect;
                } else {
                    isSubmitting = false;
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalText;
                    showAlert(result.error || 'Upload failed', 'error');
                }
            } catch (error) {
                hideSpinner();
                isSubmitting = false;
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
                showAlert('Network error. Please try again.', 'error');
                console.error('Upload error:', error);
            }
        });
    }
}

// Chart Initialization
function initCharts() {
    // Spending by Category Chart
    const categoryCanvas = document.getElementById('categoryChart');
    if (categoryCanvas && window.chartData && window.chartData.categories) {
        const ctx = categoryCanvas.getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: window.chartData.categories.labels,
                datasets: [{
                    label: 'Spending Amount (₹)',
                    data: window.chartData.categories.data,
                    backgroundColor: 'rgba(255, 214, 91, 0.8)',
                    borderColor: 'rgba(255, 214, 91, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '₹' + value.toLocaleString('en-IN');
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Spending Trend Chart
    const trendCanvas = document.getElementById('trendChart');
    if (trendCanvas && window.chartData && window.chartData.trend) {
        const ctx = trendCanvas.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: window.chartData.trend.labels,
                datasets: [{
                    label: 'Monthly Spending (₹)',
                    data: window.chartData.trend.data,
                    borderColor: 'rgba(29, 31, 33, 1)',
                    backgroundColor: 'rgba(29, 31, 33, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '₹' + value.toLocaleString('en-IN');
                            }
                        }
                    }
                }
            }
        });
    }
}

// Category Update Handler
function initCategoryUpdate() {
    const categorySelect = document.getElementById('categorySelect');
    const updateBtn = document.getElementById('updateCategoryBtn');
    
    if (categorySelect && updateBtn) {
        updateBtn.addEventListener('click', async () => {
            const newCategory = categorySelect.value;
            const index = parseInt(categorySelect.dataset.index);
            
            if (!newCategory) {
                showAlert('Please select a category', 'error');
                return;
            }
            
            try {
                const response = await fetch('/api/update_category', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ index, category: newCategory })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showAlert('Category updated successfully', 'success');
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 1000);
                } else {
                    showAlert(result.error || 'Update failed', 'error');
                }
            } catch (error) {
                showAlert('Network error. Please try again.', 'error');
                console.error('Update error:', error);
            }
        });
    }
}

// Export Data Handler
function initExport() {
    const exportBtn = document.getElementById('exportBtn');
    
    if (exportBtn) {
        exportBtn.addEventListener('click', async () => {
            try {
                const response = await fetch('/api/export');
                const data = await response.json();
                
                if (data.error) {
                    showAlert(data.error, 'error');
                    return;
                }
                
                // Create download
                const blob = new Blob([JSON.stringify(data, null, 2)], {
                    type: 'application/json'
                });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `phonepe-insights-${Date.now()}.json`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                
                showAlert('Data exported successfully', 'success');
            } catch (error) {
                showAlert('Export failed. Please try again.', 'error');
                console.error('Export error:', error);
            }
        });
    }
}

// Table Search and Filter
function initTableSearch() {
    const searchInput = document.getElementById('tableSearch');
    const table = document.querySelector('.transactions-table');
    
    if (searchInput && table) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    }
}

// Initialize all functionality
document.addEventListener('DOMContentLoaded', () => {
    initFileUpload();
    initCharts();
    initCategoryUpdate();
    initExport();
    initTableSearch();
});

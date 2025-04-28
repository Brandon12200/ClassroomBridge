/**
 * Functions for ClassroomBridge UI interactivity
 */

// Document loaded event listener
document.addEventListener('DOMContentLoaded', function() {
    // Initial setup
    checkLoginStatus();
});

/**
 * Check if user is logged in and update UI accordingly
 */
function checkLoginStatus() {
    fetch('/check_login_status')
        .then(response => response.json())
        .then(data => {
            updateUI(data.is_authenticated);
        })
        .catch(error => {
            console.error('Error checking login status:', error);
        });
}

/**
 * Update UI based on login status
 * @param {boolean} isLoggedIn - Whether user is authenticated
 */
function updateUI(isLoggedIn) {
    const loginRegisterButtons = document.querySelector('.login-and-register');
    const logoutButton = document.querySelector('.logout');
    
    if (isLoggedIn) {
        if (loginRegisterButtons) loginRegisterButtons.style.display = 'none';
        if (logoutButton) logoutButton.style.display = 'block';
    } else {
        if (loginRegisterButtons) loginRegisterButtons.style.display = 'flex';
        if (logoutButton) logoutButton.style.display = 'none';
    }
}

/**
 * Show login form overlay
 */
function showLoginForm() {
    document.getElementById('overlay').style.display = 'flex';
    document.getElementById('loginForm').style.display = 'block';
    document.getElementById('registerForm').style.display = 'none';
    document.getElementById('classForm').style.display = 'none';
    document.getElementById('to-blur').style.filter = 'blur(5px)';
}

/**
 * Show registration form overlay
 */
function showRegisterForm() {
    document.getElementById('overlay').style.display = 'flex';
    document.getElementById('registerForm').style.display = 'block';
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('classForm').style.display = 'none';
    document.getElementById('to-blur').style.filter = 'blur(5px)';
}

/**
 * Show new class form overlay
 */
function showNewClassForm() {
    document.getElementById('overlay').style.display = 'flex';
    document.getElementById('classForm').style.display = 'block';
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('registerForm').style.display = 'none';
    document.getElementById('to-blur').style.filter = 'blur(5px)';
    
    // Setup image preview for class picture
    const fileInput = document.getElementById('class_picture');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const previewContainer = document.getElementById('image-preview-container');
            const preview = document.getElementById('image-preview');
            
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    previewContainer.style.display = 'block';
                }
                
                reader.readAsDataURL(this.files[0]);
            } else {
                previewContainer.style.display = 'none';
            }
        });
    }
}

/**
 * Close overlays and return to normal view
 */
function goBack() {
    document.getElementById('overlay').style.display = 'none';
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('registerForm').style.display = 'none';
    document.getElementById('classForm').style.display = 'none';
    document.getElementById('to-blur').style.filter = 'none';
}

/**
 * Check login status and redirect to classes page if logged in
 */
function isLoggedIn() {
    fetch('/check_login_status')
        .then(response => response.json())
        .then(data => {
            if (data.is_authenticated) {
                const classesUrl = document.getElementById('view-classes-button').dataset.loginUrl;
                window.location.href = classesUrl;
            } else {
                showLoginForm();
            }
        })
        .catch(error => {
            console.error('Error checking login status:', error);
        });

// Utility functions
const AppUtils = {
    // Show an alert message with optional timeout
    showMessage: function(message, type = 'info', timeout = 3000) {
      const alertDiv = document.createElement('div');
      alertDiv.className = `alert alert-${type} position-fixed top-0 end-0 m-3`;
      alertDiv.style.zIndex = "1050";
      alertDiv.innerHTML = `<span>${message}</span>`;
      document.body.appendChild(alertDiv);
      
      setTimeout(() => {
        alertDiv.classList.add('fade-out');
        setTimeout(() => alertDiv.remove(), 300);
      }, timeout);
    },
    
    // Create a simple modal
    createModal: function(title, content, primaryBtnText, onPrimaryClick) {
      const modalId = 'app-modal-' + Date.now();
      const modalHtml = `
        <div class="modal fade" id="${modalId}" tabindex="-1" aria-hidden="true">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">${title}</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">${content}</div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-primary" id="${modalId}-primary">${primaryBtnText}</button>
              </div>
            </div>
          </div>
        </div>
      `;
      
      const modalWrapper = document.createElement('div');
      modalWrapper.innerHTML = modalHtml;
      document.body.appendChild(modalWrapper);
      
      const modalElement = document.getElementById(modalId);
      const modal = new bootstrap.Modal(modalElement);
      
      document.getElementById(`${modalId}-primary`).addEventListener('click', () => {
        onPrimaryClick();
        modal.hide();
      });
      
      modalElement.addEventListener('hidden.bs.modal', () => {
        modalElement.remove();
      });
      
      modal.show();
      return modal;
    }
  };
  
  // Form validation
  const Validator = {
    patterns: {
      email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
      notEmpty: /.+/
    },
    
    validateField: function(field) {
      const value = field.value.trim();
      const validations = field.dataset.validate ? field.dataset.validate.split(' ') : [];
      let isValid = true;
      let errorMessage = '';
      
      validations.forEach(validation => {
        if (validation === 'required' && !value) {
          isValid = false;
          errorMessage = 'This field is required';
        } else if (validation === 'email' && !this.patterns.email.test(value)) {
          isValid = false;
          errorMessage = 'Please enter a valid email address';
        }
      });
      
      this.setFieldValidity(field, isValid, errorMessage);
      return isValid;
    },
    
    setFieldValidity: function(field, isValid, message = '') {
      const feedbackElement = field.nextElementSibling?.classList.contains('invalid-feedback') 
        ? field.nextElementSibling 
        : document.createElement('div');
      
      if (!field.nextElementSibling?.classList.contains('invalid-feedback')) {
        feedbackElement.className = 'invalid-feedback';
        field.parentNode.insertBefore(feedbackElement, field.nextSibling);
      }
      
      feedbackElement.textContent = message;
      
      if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
      } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
      }
    },
    
    validateForm: function(form) {
      const fields = form.querySelectorAll('[data-validate]');
      let isFormValid = true;
      
      fields.forEach(field => {
        if (!this.validateField(field)) {
          isFormValid = false;
        }
      });
      
      return isFormValid;
    }
  };
  
  // File Upload Handler
  const FileUploader = {
    setupImageUpload: function(inputElement, previewElement) {
      const fileInput = document.getElementById(inputElement);
      const preview = document.getElementById(previewElement);
      
      if (!fileInput || !preview) return;
      
      // Create a drop zone around the preview area
      preview.classList.add('file-drop-zone');
      
      // Create a clickable button to trigger file selection
      const uploadButton = document.createElement('button');
      uploadButton.className = 'btn btn-outline-primary upload-btn';
      uploadButton.innerHTML = '<i class="bi bi-upload"></i> Upload Photo';
      uploadButton.type = 'button';
      
      // Insert the button after the preview
      preview.parentNode.insertBefore(uploadButton, preview.nextSibling);
      
      // Handle clicking on the upload button
      uploadButton.addEventListener('click', () => {
        fileInput.click();
      });
      
      // Handle drag and drop
      preview.addEventListener('dragover', (e) => {
        e.preventDefault();
        preview.classList.add('dragover');
      });
      
      preview.addEventListener('dragleave', () => {
        preview.classList.remove('dragover');
      });
      
      preview.addEventListener('drop', (e) => {
        e.preventDefault();
        preview.classList.remove('dragover');
        
        if (e.dataTransfer.files.length) {
          fileInput.files = e.dataTransfer.files;
          this.handleFileSelect(fileInput, preview);
        }
      });
      
      // Handle file selection
      fileInput.addEventListener('change', () => {
        this.handleFileSelect(fileInput, preview);
      });
      
      // Add help text
      const helpText = document.createElement('small');
      helpText.className = 'form-text text-muted mt-2 d-block';
      helpText.textContent = 'Drag and drop an image or click the button to upload';
      preview.parentNode.insertBefore(helpText, uploadButton.nextSibling);
    },
    
    handleFileSelect: function(fileInput, previewElement) {
      if (fileInput.files && fileInput.files[0]) {
        const file = fileInput.files[0];
        
        // Check if the file is an image
        if (!file.type.match('image.*')) {
          AppUtils.showMessage('Please select an image file', 'danger');
          return;
        }
        
        const reader = new FileReader();
        
        reader.onload = function(e) {
          previewElement.innerHTML = `<img src="${e.target.result}" class="img-preview" alt="Preview">`;
          previewElement.classList.add('has-preview');
          
          // Add a remove button
          const removeBtn = document.createElement('button');
          removeBtn.className = 'btn btn-sm btn-danger position-absolute top-0 end-0 m-2';
          removeBtn.innerHTML = '<i class="bi bi-x"></i>';
          removeBtn.type = 'button';
          removeBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            previewElement.innerHTML = '';
            previewElement.classList.remove('has-preview');
            fileInput.value = '';
          });
          
          previewElement.appendChild(removeBtn);
        };
        
        reader.readAsDataURL(file);
      }
    }
  };
  
  // Student Selection Enhancement
  const StudentSelector = {
    init: function(elementId) {
      const container = document.getElementById(elementId);
      if (!container) return;
      
      // Get the original input
      const originalInput = container.querySelector('input[type="text"]');
      if (!originalInput) return;
      
      // Create a styled container
      const selectorContainer = document.createElement('div');
      selectorContainer.className = 'student-selector-container';
      
      // Create a search input
      const searchInput = document.createElement('input');
      searchInput.type = 'text';
      searchInput.className = 'form-control';
      searchInput.placeholder = 'Search students by name or email';
      
      // Create a results container
      const resultsContainer = document.createElement('div');
      resultsContainer.className = 'student-search-results d-none';
      
      // Create a selected students container
      const selectedContainer = document.createElement('div');
      selectedContainer.className = 'selected-students';
      
      // Add hidden inputs container
      const hiddenInputsContainer = document.createElement('div');
      hiddenInputsContainer.className = 'hidden-inputs';
      
      // Replace the original input with our enhanced version
      originalInput.parentNode.insertBefore(selectorContainer, originalInput);
      originalInput.style.display = 'none';
      
      // Add all components to the container
      selectorContainer.appendChild(searchInput);
      selectorContainer.appendChild(resultsContainer);
      selectorContainer.appendChild(selectedContainer);
      selectorContainer.appendChild(hiddenInputsContainer);
      
      // Add event listener for search input
      searchInput.addEventListener('input', this.debounce(() => {
        this.searchStudents(searchInput.value, resultsContainer);
      }, 300));
      
      // Add event listener to show/hide results
      searchInput.addEventListener('focus', () => {
        if (searchInput.value.length > 0) {
          resultsContainer.classList.remove('d-none');
        }
      });
      
      // Close the dropdown when clicking outside
      document.addEventListener('click', (e) => {
        if (!selectorContainer.contains(e.target)) {
          resultsContainer.classList.add('d-none');
        }
      });
    },
    
    searchStudents: function(query, resultsContainer) {
      if (query.length < 2) {
        resultsContainer.classList.add('d-none');
        return;
      }
      
      // Show loading state
      resultsContainer.innerHTML = '<div class="text-center py-2"><div class="spinner-border spinner-border-sm"></div></div>';
      resultsContainer.classList.remove('d-none');
      
      // Make an AJAX request to search for students
      fetch(`/api/search-students?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
          if (data.students && data.students.length > 0) {
            this.renderResults(data.students, resultsContainer);
          } else {
            resultsContainer.innerHTML = '<div class="p-2 text-muted">No students found</div>';
          }
        })
        .catch(() => {
          resultsContainer.innerHTML = '<div class="p-2 text-danger">Error searching for students</div>';
        });
    },
    
    renderResults: function(students, resultsContainer) {
      resultsContainer.innerHTML = '';
      
      students.forEach(student => {
        const resultItem = document.createElement('div');
        resultItem.className = 'student-result-item';
        resultItem.dataset.id = student.id;
        resultItem.dataset.name = student.name;
        resultItem.dataset.email = student.email;
        
        resultItem.innerHTML = `
          <div class="d-flex align-items-center p-2 border-bottom student-result">
            <div class="me-2">
              ${student.avatar ? `<img src="${student.avatar}" class="avatar-sm rounded-circle" alt="">` : 
                `<div class="avatar-placeholder-sm rounded-circle">${student.name.charAt(0)}</div>`}
            </div>
            <div>
              <div>${student.name}</div>
              <small class="text-muted">${student.email}</small>
            </div>
          </div>
        `;
        
        resultItem.addEventListener('click', () => {
          this.addSelectedStudent(student, resultsContainer);
        });
        
        resultsContainer.appendChild(resultItem);
      });
    },
    
    addSelectedStudent: function(student, resultsContainer) {
      const selectedContainer = resultsContainer.parentNode.querySelector('.selected-students');
      const hiddenInputsContainer = resultsContainer.parentNode.querySelector('.hidden-inputs');
      
      // Check if student is already selected
      if (document.querySelector(`.selected-student[data-id="${student.id}"]`)) {
        resultsContainer.classList.add('d-none');
        return;
      }
      
      // Create the selected student element
      const selectedElement = document.createElement('div');
      selectedElement.className = 'selected-student badge bg-primary me-2 mb-2';
      selectedElement.dataset.id = student.id;
      
      selectedElement.innerHTML = `
        ${student.name}
        <button type="button" class="btn-close btn-close-white ms-2"></button>
      `;
      
      // Add a hidden input for the backend
      const hiddenInput = document.createElement('input');
      hiddenInput.type = 'hidden';
      hiddenInput.name = 'students[]';
      hiddenInput.value = student.id;
      
      // Add the remove functionality
      selectedElement.querySelector('.btn-close').addEventListener('click', () => {
        selectedElement.remove();
        hiddenInput.remove();
      });
      
      // Add to the DOM
      selectedContainer.appendChild(selectedElement);
      hiddenInputsContainer.appendChild(hiddenInput);
      
      // Clear and hide the search results
      const searchInput = resultsContainer.parentNode.querySelector('input[type="text"]');
      searchInput.value = '';
      resultsContainer.classList.add('d-none');
    },
    
    debounce: function(func, delay) {
      let timeout;
      return function() {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), delay);
      };
    }
  };
  
  // Initialize new enhancements only when explicitly called
  function initEnhancedFeatures() {
    // Initialize field validations
    document.querySelectorAll('input[data-validate], textarea[data-validate], select[data-validate]').forEach(field => {
      field.addEventListener('blur', () => {
        Validator.validateField(field);
      });
    });
    
    // Initialize file uploads where needed
    const imageUploadElements = document.querySelectorAll('[data-file-upload]');
    imageUploadElements.forEach(element => {
      const inputId = element.dataset.fileUpload;
      const previewId = element.dataset.preview;
      FileUploader.setupImageUpload(inputId, previewId);
    });
    
    // Initialize student selectors
    const studentSelectContainers = document.querySelectorAll('[data-student-selector]');
    studentSelectContainers.forEach(container => {
      StudentSelector.init(container.id);
    });
    
    // Add CSS for our components
    const style = document.createElement('style');
    style.textContent = `
      .file-drop-zone {
        border: 2px dashed #ccc;
        border-radius: 5px;
        padding: 20px;
        text-align: center;
        position: relative;
        min-height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #f8f9fa;
        transition: all 0.3s;
      }
      
      .file-drop-zone.dragover {
        background-color: #e9ecef;
        border-color: #6c757d;
      }
      
      .file-drop-zone.has-preview {
        padding: 0;
        border-style: solid;
      }
      
      .file-drop-zone .img-preview {
        max-width: 100%;
        max-height: 200px;
      }
      
      .loading-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(255, 255, 255, 0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
      }
      
      .student-selector-container {
        position: relative;
      }
      
      .student-search-results {
        position: absolute;
        left: 0;
        right: 0;
        top: 100%;
        background: white;
        border: 1px solid #ced4da;
        border-radius: 0 0 0.25rem 0.25rem;
        max-height: 300px;
        overflow-y: auto;
        z-index: 1050;
      }
      
      .student-result:hover {
        background-color: #f8f9fa;
        cursor: pointer;
      }
      
      .selected-students {
        margin-top: 10px;
        display: flex;
        flex-wrap: wrap;
      }
      
      .avatar-sm {
        width: 30px;
        height: 30px;
      }
      
      .avatar-placeholder-sm {
        width: 30px;
        height: 30px;
        background-color: #6c757d;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
      }
      
      .fade-out {
        animation: fadeOut 0.3s;
      }
      
      @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
      }
    `;
    document.head.appendChild(style);
  }
  
  // Add an initialization function that can be called after the page loads
  // This won't automatically execute, preventing conflicts with existing code
  document.addEventListener('DOMContentLoaded', function() {
    // Check if enhanced features should be initialized
    const enhancedElements = document.querySelectorAll('[data-enhanced="true"]');
    if (enhancedElements.length > 0) {
      initEnhancedFeatures();
    }
  });
  
  // Make our utilities available globally so they can be called from HTML
  window.AppUtils = AppUtils;
  window.Validator = Validator;
  window.FileUploader = FileUploader;
  window.StudentSelector = StudentSelector;
  window.initEnhancedFeatures = initEnhancedFeatures;

}
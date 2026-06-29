const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadContent = document.getElementById('uploadContent');
const imagePreview = document.getElementById('imagePreview');
const predictBtn = document.getElementById('predictBtn');
const loading = document.getElementById('loading');
const resultsSection = document.getElementById('resultsSection');
const actorNameSpan = document.getElementById('actorName');
const moviesGrid = document.getElementById('moviesGrid');
const errorMessage = document.getElementById('errorMessage');

let selectedFile = null;

// Handle click on upload area
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

// Handle drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    if (e.dataTransfer.files.length > 0) {
        handleFileSelect(e.dataTransfer.files[0]);
    }
});

// Handle file input change
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

function handleFileSelect(file) {
    // Validate file type
    if (!file.type.match('image/jpeg') && !file.type.match('image/png')) {
        showError('Please select a JPG or PNG image.');
        return;
    }
    
    selectedFile = file;
    hideError();
    
    // Preview image
    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        uploadContent.classList.add('hidden');
        imagePreview.classList.remove('hidden');
        predictBtn.disabled = false;
        
        // Hide previous results when new image is uploaded
        resultsSection.classList.add('hidden');
    };
    reader.readAsDataURL(file);
}

// Handle predict button click
predictBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    
    // UI state loading
    predictBtn.disabled = true;
    loading.classList.remove('hidden');
    resultsSection.classList.add('hidden');
    hideError();
    
    const formData = new FormData();
    formData.append('image', selectedFile);
    
    try {
        // We assume the FastAPI backend runs on localhost:8000
        const response = await fetch('http://127.0.0.1:8000/predict', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'An error occurred during prediction.');
        }
        
        displayResults(data);
    } catch (error) {
        showError(error.message);
    } finally {
        predictBtn.disabled = false;
        loading.classList.add('hidden');
    }
});

function displayResults(data) {
    actorNameSpan.textContent = data.actor;
    moviesGrid.innerHTML = '';
    
    data.movies.forEach(movie => {
        const card = document.createElement('div');
        card.className = 'movie-card';
        
        const year = movie.year ? `(${movie.year})` : '';
        const genre = movie.genre || 'Unknown genre';
        const rating = movie.rating ? movie.rating.toFixed(1) : 'N/A';
        
        card.innerHTML = `
            <div class="movie-title">${movie.title} <span style="font-size: 0.9em; font-weight: normal; color: var(--text-secondary)">${year}</span></div>
            <div class="movie-details">${genre}</div>
            <div class="movie-rating">${rating}</div>
        `;
        
        moviesGrid.appendChild(card);
    });
    
    resultsSection.classList.remove('hidden');
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function showError(msg) {
    errorMessage.textContent = msg;
    errorMessage.classList.remove('hidden');
}

function hideError() {
    errorMessage.classList.add('hidden');
}

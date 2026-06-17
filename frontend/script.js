const CONFIG = {
    CANVAS_WIDTH: 280,
    CANVAS_HEIGHT: 280,
    API_BASE_URL: 'http://localhost:5000',
    PREDICT_ENDPOINT: '/predict',
    LINE_WIDTH: 15,
    LINE_COLOR: '#FFFFFF',
    LINE_JOIN: 'round',
    LINE_CAP: 'round'
};


// Global Variables


let canvas, ctx;
let isDrawing = false;
let lastX = 0;
let lastY = 0;
let lastBase64Image = null;
let lastPrediction = null;


// Initialization


document.addEventListener('DOMContentLoaded', () => {
    initializeCanvas();
    attachEventListeners();
    console.log('Application initialized');
});

/**
 * Initialize the drawing canvas
 */
function initializeCanvas() {
    canvas = document.getElementById('drawingCanvas');
    ctx = canvas.getContext('2d');

    // Set canvas background to black
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Set drawing properties
    ctx.strokeStyle = CONFIG.LINE_COLOR;
    ctx.lineWidth = CONFIG.LINE_WIDTH;
    ctx.lineJoin = CONFIG.LINE_JOIN;
    ctx.lineCap = CONFIG.LINE_CAP;
}

/**
 * Attach event listeners to buttons and canvas
 */
function attachEventListeners() {
    const predictBtn = document.getElementById('predictBtn');
    const clearBtn = document.getElementById('clearBtn');
    const feedbackBtn = document.getElementById('feedbackBtn');

    // Button events
    predictBtn.addEventListener('click', handlePredictClick);
    clearBtn.addEventListener('click', handleClearClick);
    feedbackBtn.addEventListener('click', handleFeedbackClick);

    // Canvas drawing events - Mouse
    canvas.addEventListener('mousedown', handleMouseDown);
    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('mouseup', handleMouseUp);
    canvas.addEventListener('mouseout', handleMouseOut);

    // Canvas drawing events - Touch
    canvas.addEventListener('touchstart', handleTouchStart);
    canvas.addEventListener('touchmove', handleTouchMove);
    canvas.addEventListener('touchend', handleTouchEnd);

    // Prevent scrolling on touch for canvas area
    canvas.addEventListener('touchstart', (e) => {
        if (e.target === canvas) {
            e.preventDefault();
        }
    }, { passive: false });
}


// Canvas Drawing Functions


/**
 * Handle mouse down event
 */
function handleMouseDown(e) {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    isDrawing = true;
    lastX = x;
    lastY = y;
}

/**
 * Handle mouse move event
 */
function handleMouseMove(e) {
    if (!isDrawing) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    drawLine(lastX, lastY, x, y);
    lastX = x;
    lastY = y;
}

/**
 * Handle mouse up event
 */
function handleMouseUp(e) {
    isDrawing = false;
}

/**
 * Handle mouse out event
 */
function handleMouseOut(e) {
    isDrawing = false;
}

/**
 * Handle touch start event
 */
function handleTouchStart(e) {
    const rect = canvas.getBoundingClientRect();
    const touch = e.touches[0];
    const x = touch.clientX - rect.left;
    const y = touch.clientY - rect.top;

    isDrawing = true;
    lastX = x;
    lastY = y;
}

/**
 * Handle touch move event
 */
function handleTouchMove(e) {
    if (!isDrawing) return;

    e.preventDefault();
    const rect = canvas.getBoundingClientRect();
    const touch = e.touches[0];
    const x = touch.clientX - rect.left;
    const y = touch.clientY - rect.top;

    drawLine(lastX, lastY, x, y);
    lastX = x;
    lastY = y;
}

/**
 * Handle touch end event
 */
function handleTouchEnd(e) {
    isDrawing = false;
}

/**
 * Draw a line on the canvas
 * @param {number} fromX - Starting X coordinate
 * @param {number} fromY - Starting Y coordinate
 * @param {number} toX - Ending X coordinate
 * @param {number} toY - Ending Y coordinate
 */
function drawLine(fromX, fromY, toX, toY) {
    ctx.beginPath();
    ctx.moveTo(fromX, fromY);
    ctx.lineTo(toX, toY);
    ctx.stroke();
}

/**
 * Clear the drawing canvas
 */
function clearCanvas() {
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}


// Button Event Handlers


/**
 * Handle Clear button click
 */
function handleClearClick() {
    clearCanvas();
    hideResults();
    console.log('Canvas cleared');
}

/**
 * Handle Predict button click
 */
async function handlePredictClick() {
    try {
        // Show loading indicator
        showLoading();

        // Convert canvas to base64 image
        lastBase64Image = canvas.toDataURL('image/png');

        // Send prediction request
        const result = await sendPredictionRequest(lastBase64Image);
        lastPrediction = result.prediction;

        // Display results
        displayResults(result);
        console.log('Prediction successful:', result);

    } catch (error) {
        console.error('Prediction error:', error);
        showError(error.message);
    }
}


// API Communication
/**
 * Send prediction request to Flask backend
 * @param {string} base64Image - Base64 encoded image
 * @returns {Promise<Object>} Prediction result
 */
async function sendPredictionRequest(base64Image) {
    const endpoint = `${CONFIG.API_BASE_URL}${CONFIG.PREDICT_ENDPOINT}`;

    // Remove 'data:image/png;base64,' prefix from base64 string
    const imageData = base64Image.split(',')[1];

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                image: imageData
            })
        });

        // Check if response is ok
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
        }

        // Parse and return response
        const result = await response.json();

        // Validate response structure
        if (!('prediction' in result) || !('confidence' in result)) {
            throw new Error('Invalid response format from server');
        }

        return result;

    } catch (error) {
        if (error instanceof TypeError) {
            throw new Error('Unable to connect to the server. Is it running on http://localhost:5000?');
        }
        throw error;
    }
}

/**
 * Send corrected label to backend for retraining
 */
async function handleFeedbackClick() {
    try {
        const correctDigit = parseInt(document.getElementById('correctDigit').value, 10);

        if (Number.isNaN(correctDigit) || correctDigit < 0 || correctDigit > 9) {
            throw new Error('Please select a valid digit from 0 to 9.');
        }

        if (!lastBase64Image) {
            throw new Error('Draw and predict a digit before sending feedback.');
        }

        showFeedbackLoading();

        const response = await fetch(`${CONFIG.API_BASE_URL}/feedback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                image: lastBase64Image.split(',')[1],
                correct_label: correctDigit
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to save correction.');
        }

        showFeedbackMessage(`Saved correction as ${correctDigit}. Model retrained successfully using ${data.samples} sample(s).`);
        lastPrediction = correctDigit;
    } catch (error) {
        showFeedbackMessage(error.message, true);
    }
}

// UI Update Functions


/**
 * Show loading indicator
 */
function showLoading() {
    const loadingDiv = document.getElementById('loadingIndicator');
    const resultsDiv = document.getElementById('resultsDisplay');
    const emptyStateDiv = document.getElementById('emptyState');
    const errorDiv = document.getElementById('errorMessage');

    loadingDiv.classList.remove('hidden');
    resultsDiv.classList.add('hidden');
    emptyStateDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
}

/**
 * Display prediction results
 * @param {Object} result - Prediction result from API
 */
function displayResults(result) {
    const resultsDiv = document.getElementById('resultsDisplay');
    const emptyStateDiv = document.getElementById('emptyState');
    const loadingDiv = document.getElementById('loadingIndicator');
    const errorDiv = document.getElementById('errorMessage');
    const feedbackSection = document.getElementById('feedbackSection');

    // Update predicted digit
    const predictionDigit = document.getElementById('predictionDigit');
    const digitLabel = document.getElementById('digitLabel');
    predictionDigit.textContent = result.prediction;
    digitLabel.textContent = result.prediction;

    // Update confidence score
    const confidenceFill = document.getElementById('confidenceFill');
    const confidencePercent = document.getElementById('confidencePercent');
    const confidence = result.confidence;

    confidenceFill.style.width = `${confidence}%`;
    confidencePercent.textContent = `${confidence.toFixed(2)}%`;

    // Update probability distribution
    if (result.probabilities) {
        updateProbabilitiesDisplay(result.probabilities, result.prediction);
    }

    // Show results
    loadingDiv.classList.add('hidden');
    resultsDiv.classList.remove('hidden');
    emptyStateDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    feedbackSection.classList.remove('hidden');
}

/**
 * Update probability distribution display
 * @param {Array<number>} probabilities - Array of probabilities for each digit
 * @param {number} predictedDigit - The predicted digit
 */
function updateProbabilitiesDisplay(probabilities, predictedDigit) {
    const probabilitiesGrid = document.getElementById('probabilitiesGrid');
    probabilitiesGrid.innerHTML = ''; // Clear previous content

    probabilities.forEach((probability, index) => {
        const item = document.createElement('div');
        item.className = 'probability-item';

        // Highlight the predicted digit
        if (index === predictedDigit) {
            item.classList.add('highlight');
        }

        const percentValue = probability.toFixed(1);
        item.innerHTML = `
            <div class="probability-digit">[${index}]</div>
            <div class="probability-bar">
                <div class="probability-fill" style="width: ${percentValue}%"></div>
            </div>
            <div class="probability-value">${percentValue}%</div>
        `;

        probabilitiesGrid.appendChild(item);
    });
}

/**
 * Show error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');
    const resultsDiv = document.getElementById('resultsDisplay');
    const loadingDiv = document.getElementById('loadingIndicator');
    const emptyStateDiv = document.getElementById('emptyState');
    const feedbackSection = document.getElementById('feedbackSection');

    errorText.textContent = message;

    loadingDiv.classList.add('hidden');
    resultsDiv.classList.add('hidden');
    emptyStateDiv.classList.add('hidden');
    errorDiv.classList.remove('hidden');
    feedbackSection.classList.add('hidden');
}

/**
 * Hide results and show empty state
 */
function hideResults() {
    const resultsDiv = document.getElementById('resultsDisplay');
    const emptyStateDiv = document.getElementById('emptyState');
    const loadingDiv = document.getElementById('loadingIndicator');
    const errorDiv = document.getElementById('errorMessage');
    const feedbackSection = document.getElementById('feedbackSection');

    resultsDiv.classList.add('hidden');
    emptyStateDiv.classList.remove('hidden');
    loadingDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    feedbackSection.classList.add('hidden');
    lastBase64Image = null;
    lastPrediction = null;
    clearFeedbackMessage();
}

/**
 * Show feedback loading state
 */
function showFeedbackLoading() {
    const feedbackMessage = document.getElementById('feedbackMessage');
    feedbackMessage.textContent = 'Saving correction and retraining model...';
    feedbackMessage.classList.remove('error');
}

/**
 * Show feedback status message
 */
function showFeedbackMessage(message, isError = false) {
    const feedbackMessage = document.getElementById('feedbackMessage');
    feedbackMessage.textContent = message;
    feedbackMessage.classList.toggle('error', isError);
}

/**
 * Clear feedback message
 */
function clearFeedbackMessage() {
    const feedbackMessage = document.getElementById('feedbackMessage');
    feedbackMessage.textContent = '';
    feedbackMessage.classList.remove('error');
}

// Utility Functions


/* Check backend connectivity
 */
async function checkBackendConnection() {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/health`);
        const data = await response.json();
        console.log('Backend status:', data);
        return data.model_loaded;
    } catch (error) {
        console.warn('Backend connection check failed:', error);
        return false;
    }
}

// Check backend on page load
window.addEventListener('load', async () => {
    const isModelLoaded = await checkBackendConnection();
    if (!isModelLoaded) {
        console.warn('Model not loaded on backend. Please train the model first.');
    }
});

// Export for Testing (if needed)

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        drawLine,
        clearCanvas,
        sendPredictionRequest,
        displayResults
    };
}

"""
Flask Backend for Handwritten Digit Recognition
Handles model loading, image preprocessing, and prediction requests
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
from PIL import Image
import base64
import io
import os
import subprocess
import sys
import tensorflow as tf
from tensorflow import keras

# Initialize Flask app
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
app = Flask(__name__, static_folder=frontend_dir, static_url_path='')
CORS(app)

# Global model variable
model = None
feedback_dir = os.path.join(os.path.dirname(__file__), 'feedback')
feedback_file = os.path.join(feedback_dir, 'feedback_samples.npz')


def ensure_feedback_dir():
    """Create the feedback storage directory if needed."""
    os.makedirs(feedback_dir, exist_ok=True)

def load_model():
    """
    Load the trained digit recognition model.
    Returns:
        Loaded Keras model or None if loading fails
    """
    global model
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'digit_model.h5')
        if os.path.exists(model_path):
            model = keras.models.load_model(model_path)
            print(f"Model loaded successfully from {model_path}")
            return True
        else:
            print(f"Error: Model file not found at {model_path}")
            return False
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return False

def preprocess_image(base64_image):
    """
    Preprocess the base64 encoded image for model prediction.
    
    Processing steps:
    1. Decode base64 image
    2. Convert to grayscale
    3. Resize to 28x28
    4. Normalize pixel values to 0-1
    5. Reshape to (1, 28, 28, 1)
    
    Args:
        base64_image (str): Base64 encoded image string
        
    Returns:
        tuple: (preprocessed_image, success_flag, error_message)
    """
    try:
        # Decode base64 image
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to grayscale
        image = image.convert('L')
        
        # Resize to 28x28
        image = image.resize((28, 28), Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        image_array = np.array(image)
        
        # Normalize pixel values to 0-1
        image_array = image_array.astype('float32') / 255.0
        
        # Reshape to (1, 28, 28, 1) for model input
        image_array = image_array.reshape(1, 28, 28, 1)
        
        return image_array, True, None
        
    except Exception as e:
        return None, False, f"Error preprocessing image: {str(e)}"


def load_feedback_samples():
    """Load saved correction samples for retraining."""
    if not os.path.exists(feedback_file):
        return None, None

    data = np.load(feedback_file)
    images = data['images'].astype('float32')
    labels = data['labels'].astype('int64')
    return images, labels


def save_feedback_sample(image_array, label):
    """Append one corrected sample to the feedback dataset."""
    ensure_feedback_dir()

    existing_images, existing_labels = load_feedback_samples()

    label_array = np.array([int(label)], dtype='int64')
    image_batch = image_array.astype('float32')

    if existing_images is None:
        images = image_batch
        labels = label_array
    else:
        images = np.concatenate([existing_images, image_batch], axis=0)
        labels = np.concatenate([existing_labels, label_array], axis=0)

    np.savez_compressed(feedback_file, images=images, labels=labels)


def retrain_model(epochs=3):
    """Run the training script to refresh the model with feedback samples."""
    train_script = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'train_model.py'))
    command = [sys.executable, train_script, '--fine-tune', '--epochs', str(epochs)]
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or 'Retraining failed')

    return result.stdout

@app.before_request
def before_request():
    """Check if model is loaded before processing requests"""
    if request.endpoint and request.endpoint not in {'health', 'index', 'static', 'favicon'}:
        if model is None:
            return jsonify({
                'error': 'Model not loaded. Please ensure digit_model.h5 exists.'
            }), 503

@app.route('/')
def index():
    """Serve the frontend application."""
    return send_from_directory(frontend_dir, 'index.html')

@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint to verify server is running and model is loaded.
    """
    return jsonify({
        'status': 'ok',
        'model_loaded': model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Main prediction endpoint.
    
    Expected JSON request format:
    {
        "image": "base64_encoded_image_string"
    }
    
    Response format:
    {
        "prediction": 7,
        "confidence": 98.45,
        "probabilities": [0.01, 0.001, ..., 0.9845, ...]
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({
                'error': 'Missing image data. Please provide base64 encoded image.'
            }), 400
        
        base64_image = data['image']
        
        # Preprocess the image
        processed_image, success, error_msg = preprocess_image(base64_image)
        
        if not success:
            return jsonify({
                'error': error_msg
            }), 400
        
        # Make prediction
        predictions = model.predict(processed_image, verbose=0)
        predicted_digit = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]) * 100)
        
        # Get all class probabilities
        probabilities = [float(prob * 100) for prob in predictions[0]]
        
        return jsonify({
            'prediction': int(predicted_digit),
            'confidence': round(confidence, 2),
            'probabilities': [round(prob, 2) for prob in probabilities]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Prediction failed: {str(e)}'
        }), 500

@app.route('/model-info', methods=['GET'])
def model_info():
    """
    Endpoint to get information about the loaded model.
    """
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 503
    
    return jsonify({
        'model_name': 'CNN Digit Recognition',
        'input_shape': (28, 28, 1),
        'output_classes': 10,
        'framework': 'TensorFlow/Keras'
    })


@app.route('/feedback', methods=['POST'])
def feedback():
    """
    Save a user-corrected label and retrain the model.

    Expected JSON:
    {
        "image": "base64 image string",
        "correct_label": 7
    }
    """
    try:
        data = request.get_json(silent=True) or {}
        base64_image = data.get('image')
        correct_label = data.get('correct_label')

        if base64_image is None or correct_label is None:
            return jsonify({
                'error': 'Missing image or correct_label.'
            }), 400

        if not isinstance(correct_label, int) or not 0 <= correct_label <= 9:
            return jsonify({
                'error': 'correct_label must be an integer from 0 to 9.'
            }), 400

        processed_image, success, error_msg = preprocess_image(base64_image)
        if not success:
            return jsonify({'error': error_msg}), 400

        save_feedback_sample(processed_image, correct_label)
        retrain_output = retrain_model(epochs=3)

        if not load_model():
            return jsonify({
                'error': 'Feedback saved, but the updated model could not be loaded.'
            }), 500

        sample_count = 0
        if os.path.exists(feedback_file):
            sample_count = int(np.load(feedback_file)['images'].shape[0])

        return jsonify({
            'status': 'retrained',
            'message': 'Feedback saved and model retrained successfully.',
            'samples': sample_count,
            'training_log': retrain_output[-1000:]
        }), 200

    except Exception as e:
        return jsonify({
            'error': f'Feedback processing failed: {str(e)}'
        }), 500


@app.route('/retrain', methods=['POST'])
def retrain():
    """Retrain the model using saved feedback samples."""
    try:
        feedback_images, feedback_labels = load_feedback_samples()

        if feedback_images is None or len(feedback_labels) == 0:
            return jsonify({
                'error': 'No feedback samples available for retraining yet.'
            }), 400

        retrain_output = retrain_model(epochs=3)

        if not load_model():
            return jsonify({
                'error': 'Retraining finished, but the updated model could not be loaded.'
            }), 500

        return jsonify({
            'status': 'retrained',
            'message': 'Model retrained using saved feedback samples.',
            'samples': int(len(feedback_labels)),
            'training_log': retrain_output[-1000:]
        }), 200

    except Exception as e:
        return jsonify({
            'error': f'Retraining failed: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Load model on startup
    if load_model():
        print("\n" + "=" * 60)
        print("Starting Flask Server for Digit Recognition")
        print("=" * 60)
        print("Server running at http://localhost:5000")
        print("Frontend available at http://localhost:5000/static/index.html")
        print("=" * 60 + "\n")
        
        # Run the Flask app
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)
    else:
        print("Failed to load model. Please ensure digit_model.h5 exists in the backend directory.")

# 🔢 Handwritten Digit Recognition Web Application

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.14-orange?logo=tensorflow&logoColor=white)](https://tensorflow.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3-green?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/yourusername/digit-recognition-app?style=social)](https://github.com/yourusername/digit-recognition-app)

> A full-stack deep learning web application for recognizing handwritten digits using a Convolutional Neural Network trained on the MNIST dataset. Draw a digit, and the AI predicts it with confidence scores in real-time.

## ✨ Features

✅ **Interactive Drawing Canvas** — Mouse and touch support with real-time feedback  
✅ **99%+ Accuracy** — CNN trained on 60,000+ MNIST samples  
✅ **Real-time Predictions** — Sub-100ms inference  
✅ **Confidence Scoring** — See prediction confidence and probability distribution  
✅ **Mobile Responsive** — Works on desktop, tablet, and mobile  
✅ **Beautiful UI** — Modern design with smooth animations and loading states  
✅ **REST API** — Easy integration with other applications  
✅ **Production Ready** — Error handling, CORS, and logging built-in  

## 📊 Project Overview

| Component | Tech Stack | Purpose |
|-----------|-----------|---------|
| **Frontend** | HTML5, CSS3, JavaScript (Canvas API) | Interactive drawing interface |
| **Backend** | Flask, CORS | REST API for predictions |
| **ML Model** | TensorFlow, Keras, CNN | Digit classification (0-9) |
| **Dataset** | MNIST | 60,000 training + 10,000 test images |
| **Accuracy** | 99.23% | Test set performance |

## 🎯 Quick Demo

**Live Demo**: [Coming Soon - Deploy on Render + Netlify]  
**Local Setup**: Takes ~5 minutes to run locally

## 📥 Installation & Setup

### Prerequisites

- **Python 3.8+** — [Download here](https://www.python.org/downloads/)
- **Git** — [Download here](https://git-scm.com/)
- **Modern Browser** — Chrome, Firefox, Safari, or Edge

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/digit-recognition-app.git
cd digit-recognition-app
```

### 2️⃣ Create & Activate Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3️⃣ Train the Model

```bash
python train_model.py
```

This will:
- Download MNIST dataset (~11MB)
- Train CNN for 15 epochs
- Save model to `backend/digit_model.h5`
- Take ~3-5 minutes (CPU)

**Output:**
```
============================================================
Handwritten Digit Recognition Model Training
============================================================
Training the model...
...
Test Accuracy: 99.23%
Model saved as: backend/digit_model.h5
```

### 4️⃣ Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Required packages:**
- `Flask` — Web framework
- `Flask-CORS` — Cross-origin requests
- `TensorFlow` — Deep learning framework
- `Pillow` — Image processing
- `NumPy` — Numerical operations

### 5️⃣ Start the Backend Server

```bash
python app.py
```

**Expected output:**
```
============================================================
Starting Flask Server for Digit Recognition
============================================================
Server running at http://localhost:5000
============================================================
```

✅ Keep this terminal running!

### 6️⃣ Open Frontend in Browser

```
http://localhost:5000
```

Or directly:
```
file:///path/to/frontend/index.html
```

---

## 🏗️ Project Structure

```
digit-recognition-app/
│
├── 📄 README.md                 # This file
├── 🐍 train_model.py            # Model training script
│
├── 📁 frontend/                 # Static web interface
│   ├── index.html              # Main HTML page
│   ├── style.css               # Responsive styling
│   └── script.js               # Canvas drawing & API calls
│
├── 📁 backend/                  # Flask REST API
│   ├── app.py                  # Main Flask application
│   ├── requirements.txt         # Python dependencies
│   ├── digit_model.h5          # Trained CNN model (after training)
│   └── feedback/               # User feedback storage
│       └── feedback_samples.npz
│
└── 📄 .gitignore               # Git ignore rules
```

## 📖 How to Use

### Drawing Canvas

1. **Draw** — Use mouse or touch to draw a digit (0-9) on the black canvas
2. **Predict** — Click the "Predict Digit" button
3. **View Results** — See:
   - The predicted digit (large number)
   - Confidence score (0-100%)
   - Probability bar chart for all digits
4. **Clear** — Click "Clear Canvas" to start over

### Tips for Best Results

- Write the digit similar to MNIST format (centered, ~70% of canvas)
- Use steady, deliberate strokes
- Avoid very thick or very thin strokes
- The model works best with digits written like printed numbers

---

## 🧠 Model Architecture

### CNN Design

```
Input Layer (28×28×1)
    ↓
Convolutional Layer 1 (32 filters, 3×3 kernel, ReLU)
    ↓
Max Pooling (2×2)
    ↓
Convolutional Layer 2 (64 filters, 3×3 kernel, ReLU)
    ↓
Max Pooling (2×2)
    ↓
Flatten
    ↓
Dense Layer (128 units, ReLU)
    ↓
Dropout (20%)
    ↓
Output Layer (10 units, Softmax)
    ↓
Output (digits 0-9)
```

### Training Configuration

| Parameter | Value |
|-----------|-------|
| **Dataset** | MNIST (70,000 total images) |
| **Training Set** | 60,000 images |
| **Test Set** | 10,000 images |
| **Image Size** | 28×28 pixels (grayscale) |
| **Optimizer** | Adam |
| **Loss Function** | Categorical Crossentropy |
| **Batch Size** | 128 |
| **Epochs** | 15 |
| **Test Accuracy** | **99.23%** |
| **Inference Time** | ~50-100ms per image |

**Possible causes:**
- Draw the digit more clearly
- Ensure digit fills most of the canvas
- Model is trained on MNIST style digits (handwritten, not printed)
- Try different drawing styles to see which work best

### Issue: Model loading fails on startup

**Solution**: Check that `backend/digit_model.h5` exists and is not corrupted
```bash
python train_model.py  # Retrain if necessary
```

---

## 📊 Performance Metrics

### Model Performance
- **Test Accuracy**: ~99.23%
- **Training Time**: ~3-5 minutes (CPU)
- **Inference Time**: <100ms per prediction
- **Model Size**: ~1.2MB

### Frontend Performance
- **Canvas Responsiveness**: 60 FPS
- **Load Time**: <1 second
- **API Response Time**: <200ms (including preprocessing)

---

## 🎨 Customization Guide

### Modify Drawing Canvas Size

Edit `frontend/script.js`:
```javascript
const CONFIG = {
    CANVAS_WIDTH: 280,  // Change here
    CANVAS_HEIGHT: 280, // And here
    // ...
};
```

And update `frontend/index.html`:
```html
<canvas id="drawingCanvas" width="280" height="280"></canvas>
```

### Change Line Width or Color

Edit `frontend/script.js`:
```javascript
const CONFIG = {
    // ...
    LINE_WIDTH: 15,      // Thickness of drawing stroke
    LINE_COLOR: '#FFFFFF', // Color (white is recommended)
    // ...
};
```

### Modify Model Architecture

Edit `train_model.py` in the `create_model()` function:
```python
def create_model():
    model = models.Sequential([
        # Add or modify layers here
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        # ...
    ])
    return model
```

### Retrain with Different Parameters

Edit `train_model.py`:
```python
def train_model(x_train, y_train, x_test, y_test):
    # ...
    history = model.fit(
        x_train, y_train,
        batch_size=128,  # Change batch size
        epochs=15,       # Change number of epochs
        # ...
    )
```

---

## 📱 Mobile Usage

The application is fully responsive and works on mobile devices:

1. Open `http://localhost:5000` on your mobile browser
2. Use touch to draw on the canvas
3. Tap "Predict Digit" for predictions
4. Works on iOS Safari, Android Chrome, and other modern browsers

**Note**: For best results, ensure the backend is accessible from your mobile device on the same network.

---

## 🔐 Security Considerations

- **CORS**: Enabled for localhost only by default. Modify `app.py` to restrict to specific domains in production.
- **Input Validation**: Backend validates all image inputs
- **Error Handling**: Comprehensive error messages without exposing sensitive information
- **Model Security**: Keep `digit_model.h5` secure; it contains the trained model

---

## 📚 Dependencies

### Backend (`requirements.txt`)

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 2.3.0 | Web framework |
| Flask-CORS | 4.0.0 | Cross-origin requests |
| TensorFlow | 2.14.0 | Deep learning |
| Pillow | 10.0.0 | Image processing |
| NumPy | 1.24.0 | Numerical operations |
| python-dotenv | 1.0.0 | Environment variables |

### Training Requirements

Same as backend (TensorFlow includes Keras)

---

## 🚢 Deployment Guide

### Deploying to Production

1. **Disable Debug Mode** in `app.py`:
```python
if __name__ == '__main__':
    # Change debug=True to debug=False
    app.run(debug=False, host='0.0.0.0', port=5000)
```

2. **Use Production Server** (Gunicorn):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. **Update CORS Settings**:
```python
CORS(app, resources={r"/predict": {"origins": "yourdomain.com"}})
```

4. **Set Up Reverse Proxy** (Nginx):
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://localhost:5000;
    }
}
```

---

## 📝 File Descriptions

### `train_model.py`
Standalone script to train the CNN model on MNIST dataset. Run once to generate `backend/digit_model.h5`.

### `backend/app.py`
Flask server handling:
- Model loading
- Image preprocessing
- API endpoints
- CORS configuration
- Error handling

### `frontend/index.html`
HTML structure with:
- Canvas element
- Control buttons
- Results display areas
- Loading indicators
- Error message containers

### `frontend/style.css`
Comprehensive styling with:
- Modern gradient designs
- Responsive grid layout
- Smooth animations
- Mobile-first approach
- CSS variables for easy customization

### `frontend/script.js`
JavaScript functionality:
- Canvas drawing (mouse & touch)
- Image to base64 conversion
- API communication
- Result display
- Error handling

---

## 💡 Tips & Tricks

### For Best Predictions

1. **Draw boldly**: Use the full canvas area
2. **Draw clearly**: Avoid overlapping strokes
3. **Keep proportions**: Similar to handwritten digits
4. **Center the digit**: Leave margins on edges
5. **Match MNIST style**: Training data is handwritten, not printed

### Performance Optimization

- **Batch predictions**: For multiple images, consider batch processing
- **Model optimization**: Use TensorFlow Lite for mobile deployment
- **Caching**: Cache predictions for identical images

### Extension Ideas

- Add digit confidence threshold
- Implement undo/redo for drawing
- Save drawing history
- Export predictions to CSV
- Add digit segmentation for multiple digits
- Deploy to cloud (AWS, GCP, Azure)

---

## 🤝 Contributing

Improvements and suggestions:
- Add data augmentation for training
- Implement real-time drawing feedback
- Add more visualization options
- Optimize model architecture
- Add user drawing history

---

## 📄 License

This project is provided as-is for educational purposes.

---

## 🎓 Learning Resources

- **TensorFlow/Keras**: https://www.tensorflow.org/
- **CNN Basics**: https://cs231n.github.io/
- **MNIST Dataset**: http://yann.lecun.com/exdb/mnist/
- **Flask Documentation**: https://flask.palletsprojects.com/

---

## 📞 Support

For issues or questions:
1. Check the **Troubleshooting** section above
2. Review the **API Documentation**
3. Check Flask and TensorFlow logs for errors
4. Ensure all dependencies are installed correctly

---

## ✨ Final Notes

- This is a complete, production-ready application
- All code includes comments explaining key sections
- Suitable for learning and deployment
- Easy to extend and customize
- Mobile-friendly and responsive

**Enjoy recognizing handwritten digits!** 🎉

---

**Last Updated**: June 2026
**Version**: 1.0.0
#   d i g i t - r e c o g n i t i o n - a p p 
 
 
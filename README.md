# 🔢 Handwritten Digit Recognition using CNN

A full-stack AI-powered web application that recognizes handwritten digits (0–9) using a Convolutional Neural Network (CNN) trained on the MNIST dataset.

---

## 🚀 Live Demo

**Application:** https://digit-recognition-app-fn74.onrender.com

---

## 📌 Features

* 🎨 Interactive drawing canvas
* 🤖 CNN-based digit recognition
* ⚡ Real-time predictions
* 📊 Confidence score visualization
* 📱 Mobile-friendly responsive design
* 🔗 REST API powered by Flask
* ☁️ Deployed on Render

---

## 🖼️ Application Workflow

1. User draws a digit on the canvas.
2. Frontend converts the drawing into an image.
3. Image is sent to the Flask backend.
4. CNN model processes the image.
5. Predicted digit and confidence score are displayed.

---

## 🛠️ Tech Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Canvas API

### Backend

* Flask
* Flask-CORS

### Machine Learning

* TensorFlow
* Keras
* CNN (Convolutional Neural Network)

### Deployment

* Render

---

## 📂 Project Structure

```text
digit-recognition-app/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── digit_model.h5
│
├── train_model.py
├── README.md
└── .gitignore
```

---

## 🧠 Model Architecture

```text
Input (28x28x1)
      ↓
Conv2D (32 Filters)
      ↓
MaxPooling
      ↓
Conv2D (64 Filters)
      ↓
MaxPooling
      ↓
Flatten
      ↓
Dense (128)
      ↓
Dropout
      ↓
Dense (10 Softmax)
```

### Dataset

* MNIST Dataset
* 60,000 Training Images
* 10,000 Testing Images

### Performance

* Accuracy: ~99%
* Inference Time: <100ms

---

## ⚙️ Local Setup

### Clone Repository

```bash
git clone https://github.com/rudra3086/digit-recognition-app.git
cd digit-recognition-app
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Train Model

```bash
python train_model.py
```

### Run Application

```bash
python app.py
```

Open:

```text
http://localhost:5000
```

---

## 📡 API Endpoint

### Predict Digit

```http
POST /predict
```

Request:

```json
{
  "image": "<base64_image>"
}
```

Response:

```json
{
  "prediction": 7,
  "confidence": 98.42
}
```

---

## 🎯 Future Improvements

* User feedback learning
* Multiple digit recognition
* TensorFlow Lite optimization
* Model monitoring dashboard
* Docker deployment

---

## 👨‍💻 Author

**Rudra Patel**

Computer Science Engineering Student | AI/ML Enthusiast | Full Stack Developer

GitHub: https://github.com/rudra3086

---

## 📄 License

This project is intended for educational and learning purposes.

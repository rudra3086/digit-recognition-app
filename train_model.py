"""
Handwritten Digit Recognition Model Training Script
This script trains a CNN model on the MNIST dataset and saves it as digit_model.h5.
It can also fine-tune the existing model with saved correction samples.
"""

import argparse
import os

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

def create_model():
    """
    Create a CNN model for digit recognition.
    Architecture:
    - Conv2D(32, 3x3, ReLU)
    - MaxPooling2D
    - Conv2D(64, 3x3, ReLU)
    - MaxPooling2D
    - Flatten
    - Dense(128, ReLU)
    - Dense(10, Softmax)
    """
    model = models.Sequential([
        # First Convolutional Block
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2)),
        
        # Second Convolutional Block
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Flatten and Dense Layers
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    
    return model


def load_feedback_samples(feedback_path):
    """Load correction samples saved by the backend, if any exist."""
    if not os.path.exists(feedback_path):
        return None, None

    data = np.load(feedback_path)
    images = data['images'].astype('float32')
    labels = data['labels'].astype('int64')
    return images, labels

def prepare_data():
    """
    Load and preprocess MNIST dataset.
    Returns:
        x_train, y_train, x_test, y_test: Preprocessed training and test data
    """
    # Load MNIST dataset
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    
    # Normalize pixel values to 0-1 range
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0
    
    # Reshape to add channel dimension (28, 28) -> (28, 28, 1)
    x_train = x_train.reshape(-1, 28, 28, 1)
    x_test = x_test.reshape(-1, 28, 28, 1)
    
    # Convert labels to one-hot encoding
    y_train = to_categorical(y_train, 10)
    y_test = to_categorical(y_test, 10)
    
    print(f"Training data shape: {x_train.shape}")
    print(f"Test data shape: {x_test.shape}")
    
    return x_train, y_train, x_test, y_test

def train_model(x_train, y_train, x_test, y_test, epochs=15, fine_tune=False, model_path=None):
    """
    Train the CNN model.
    """
    if fine_tune and model_path and os.path.exists(model_path):
        model = keras.models.load_model(model_path)
    else:
        model = create_model()

    learning_rate = 1e-4 if fine_tune else 1e-3
    
    # Compile the model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Print model summary
    model.summary()
    
    # Train the model
    print("\nTraining the model...")
    history = model.fit(
        x_train, y_train,
        batch_size=128,
        epochs=epochs,
        verbose=1,
        validation_data=(x_test, y_test)
    )
    
    # Evaluate on test set
    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
    print(f"\nTest Accuracy: {test_accuracy * 100:.2f}%")
    print(f"Test Loss: {test_loss:.4f}")
    
    return model, history


def build_training_data(feedback_path):
    """Prepare MNIST data and merge any saved correction samples into training."""
    x_train, y_train, x_test, y_test = prepare_data()

    feedback_images, feedback_labels = load_feedback_samples(feedback_path)
    if feedback_images is not None and len(feedback_labels) > 0:
        feedback_labels = to_categorical(feedback_labels, 10)
        x_train = np.concatenate([x_train, feedback_images], axis=0)
        y_train = np.concatenate([y_train, feedback_labels], axis=0)
        print(f"Loaded {len(feedback_labels)} feedback sample(s) for retraining.")

    return x_train, y_train, x_test, y_test


def parse_args():
    """Parse command-line options for training and fine-tuning."""
    parser = argparse.ArgumentParser(description='Train or fine-tune the digit recognition model.')
    parser.add_argument('--epochs', type=int, default=15, help='Number of epochs to train.')
    parser.add_argument('--fine-tune', action='store_true', help='Continue training from an existing model if available.')
    parser.add_argument('--feedback-path', default=os.path.join(os.path.dirname(__file__), 'backend', 'feedback', 'feedback_samples.npz'))
    parser.add_argument('--model-path', default=os.path.join(os.path.dirname(__file__), 'backend', 'digit_model.h5'))
    return parser.parse_args()

def main():
    """
    Main function to orchestrate model training and saving.
    """
    print("=" * 60)
    print("Handwritten Digit Recognition Model Training")
    print("=" * 60)
    
    args = parse_args()

    # Prepare data
    print("\nPreparing MNIST dataset...")
    x_train, y_train, x_test, y_test = build_training_data(args.feedback_path)
    
    # Train model
    model, history = train_model(
        x_train,
        y_train,
        x_test,
        y_test,
        epochs=args.epochs,
        fine_tune=args.fine_tune,
        model_path=args.model_path
    )
    
    # Save model
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.makedirs(backend_dir, exist_ok=True)
    
    model.save(args.model_path)
    print(f"\nModel saved as: {args.model_path}")
    
    print("\n" + "=" * 60)
    print("Training completed successfully!")
    print("=" * 60)

if __name__ == '__main__':
    main()

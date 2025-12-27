"""
QSVM Model Module for Fraud Detection

This module contains functions to train and use a Quantum Support Vector Machine
for fraud detection on credit card transaction data.

Based on the implementation from qsvm-1.ipynb using:
- Qiskit Machine Learning with ZZFeatureMap
- FidelityQuantumKernel
- Scikit-learn SVC with precomputed kernel
"""

import numpy as np
import pandas as pd
import pickle
import os
from qiskit.circuit.library import ZZFeatureMap
from qiskit_machine_learning.kernels import FidelityQuantumKernel
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Constants
MODEL_FILE = "qsvm_model.pkl"
KERNEL_FILE = "quantum_kernel.pkl"
FEATURE_MAP_FILE = "feature_map.pkl"
X_TRAIN_FILE = "X_train.pkl"

def load_and_prepare_data(csv_path="creditcard.csv", sample_size=50, random_state=42):
    """
    Load the credit card dataset and prepare a balanced sample.
    
    Args:
        csv_path: Path to the creditcard.csv file
        sample_size: Number of samples to take from each class (fraud/normal)
        random_state: Random seed for reproducibility
    
    Returns:
        X: Feature matrix (numpy array) with V1 and V2 columns
        y: Target vector (numpy array) with Class labels
    """
    df = pd.read_csv(csv_path)
    
    # Separate fraud and normal transactions
    fraud = df[df["Class"] == 1]
    normal = df[df["Class"] == 0]
    
    # Sample equal numbers from each class
    fraud_sample = fraud.sample(n=min(sample_size, len(fraud)), random_state=random_state)
    normal_sample = normal.sample(n=min(sample_size, len(normal)), random_state=random_state)
    
    # Combine samples
    small_df = pd.concat([fraud_sample, normal_sample])
    
    # Extract features (V1 and V2 only, as in the notebook)
    X = small_df[["V1", "V2"]].values
    y = small_df["Class"].values
    
    return X, y


def train_qsvm_model(csv_path="creditcard.csv", test_size=0.3, random_state=42, sample_size=50):
    """
    Train a QSVM model for fraud detection.
    
    Args:
        csv_path: Path to the creditcard.csv file
        test_size: Proportion of data to use for testing
        random_state: Random seed for reproducibility
        sample_size: Number of samples to take from each class
    
    Returns:
        model: Trained SVC model
        quantum_kernel: Trained quantum kernel
        feature_map: The feature map used
        X_train: Training features
        X_test: Test features
        y_train: Training labels
        y_test: Test labels
    """
    print("Loading and preparing data...")
    X, y = load_and_prepare_data(csv_path, sample_size, random_state)
    
    print("Splitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    print("Creating quantum feature map...")
    # Create feature map (using V1 and V2, so feature_dimension=2)
    feature_map = ZZFeatureMap(
        feature_dimension=2,
        reps=2
    )
    
    print("Creating quantum kernel...")
    quantum_kernel = FidelityQuantumKernel(
        feature_map=feature_map
    )
    
    print("Computing training kernel matrix...")
    K_train = quantum_kernel.evaluate(X_train)
    
    print("Training QSVM model...")
    qsvm = SVC(kernel="precomputed")
    qsvm.fit(K_train, y_train)
    
    print("Computing test kernel matrix...")
    K_test = quantum_kernel.evaluate(X_test, X_train)
    
    print("Evaluating model...")
    y_pred = qsvm.predict(K_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.4f}")
    
    return qsvm, quantum_kernel, feature_map, X_train, X_test, y_train, y_test


def save_model(model, quantum_kernel, feature_map, X_train):
    """
    Save the trained model and related components to disk.
    
    Args:
        model: Trained SVC model
        quantum_kernel: Trained quantum kernel
        feature_map: The feature map used
        X_train: Training features (needed for prediction)
    """
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(model, f)
    
    with open(KERNEL_FILE, 'wb') as f:
        pickle.dump(quantum_kernel, f)
    
    with open(FEATURE_MAP_FILE, 'wb') as f:
        pickle.dump(feature_map, f)
    
    with open(X_TRAIN_FILE, 'wb') as f:
        pickle.dump(X_train, f)
    
    print(f"Model saved to {MODEL_FILE}")


def load_model():
    """
    Load the trained model and related components from disk.
    
    Returns:
        model: Trained SVC model
        quantum_kernel: Trained quantum kernel
        feature_map: The feature map used
        X_train: Training features
    """
    with open(MODEL_FILE, 'rb') as f:
        model = pickle.load(f)
    
    with open(KERNEL_FILE, 'rb') as f:
        quantum_kernel = pickle.load(f)
    
    with open(FEATURE_MAP_FILE, 'rb') as f:
        feature_map = pickle.load(f)
    
    with open(X_TRAIN_FILE, 'rb') as f:
        X_train = pickle.load(f)
    
    print(f"Model loaded from {MODEL_FILE}")
    return model, quantum_kernel, feature_map, X_train


def predict_single(model, quantum_kernel, X_train, v1, v2):
    """
    Predict fraud status for a single transaction.
    
    Args:
        model: Trained SVC model
        quantum_kernel: Trained quantum kernel
        X_train: Training features (needed for kernel evaluation)
        v1: V1 feature value
        v2: V2 feature value
    
    Returns:
        prediction: 0 (Not Fraud) or 1 (Fraud)
        probability: Confidence score (if available)
    """
    # Create feature vector
    X_new = np.array([[v1, v2]])
    
    # Compute kernel matrix between new point and training data
    K_new = quantum_kernel.evaluate(X_new, X_train)
    
    # Predict
    prediction = model.predict(K_new)[0]
    
    # Try to get probability if model supports it
    try:
        probability = model.predict_proba(K_new)[0]
        confidence = max(probability)
    except:
        confidence = None
    
    return int(prediction), confidence


def predict_batch(model, quantum_kernel, X_train, X_new):
    """
    Predict fraud status for multiple transactions.
    
    Args:
        model: Trained SVC model
        quantum_kernel: Trained quantum kernel
        X_train: Training features
        X_new: New feature matrix (n_samples, 2) with V1 and V2 columns
    
    Returns:
        predictions: Array of predictions (0 or 1)
    """
    # Ensure X_new has correct shape
    if X_new.shape[1] != 2:
        raise ValueError("X_new must have exactly 2 columns (V1 and V2)")
    
    # Compute kernel matrix
    K_new = quantum_kernel.evaluate(X_new, X_train)
    
    # Predict
    predictions = model.predict(K_new)
    
    return predictions.astype(int)


def get_or_train_model(csv_path="creditcard.csv", retrain=False):
    """
    Get the trained model, training it if it doesn't exist or if retrain=True.
    
    Args:
        csv_path: Path to the creditcard.csv file
        retrain: If True, retrain the model even if it exists
    
    Returns:
        model: Trained SVC model
        quantum_kernel: Trained quantum kernel
        feature_map: The feature map used
        X_train: Training features
    """
    if retrain or not os.path.exists(MODEL_FILE):
        print("Training new model...")
        model, quantum_kernel, feature_map, X_train, _, _, _ = train_qsvm_model(csv_path)
        save_model(model, quantum_kernel, feature_map, X_train)
    else:
        print("Loading existing model...")
        model, quantum_kernel, feature_map, X_train = load_model()
    
    return model, quantum_kernel, feature_map, X_train


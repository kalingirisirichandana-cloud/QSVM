"""
Flask Web Application for QSVM Fraud Detection

This application provides a web interface for detecting fraud in credit card
transactions using a Quantum Support Vector Machine (QSVM).

Usage:
    python app.py
    # or
    flask run

The application will:
1. Train or load a QSVM model at startup
2. Accept single transaction predictions via form
3. Accept batch predictions via CSV upload
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pandas as pd
import numpy as np
from qsvm_model import get_or_train_model, predict_single, predict_batch

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Global variables to store the model (loaded at startup)
model = None
quantum_kernel = None
feature_map = None
X_train = None


def init_model():
    """Initialize the QSVM model at application startup."""
    global model, quantum_kernel, feature_map, X_train
    
    csv_path = "creditcard.csv"
    if not os.path.exists(csv_path):
        print(f"Warning: {csv_path} not found. Please ensure the dataset is in the project directory.")
        return False
    
    try:
        model, quantum_kernel, feature_map, X_train = get_or_train_model(csv_path, retrain=False)
        print("Model initialized successfully!")
        return True
    except Exception as e:
        print(f"Error initializing model: {e}")
        import traceback
        traceback.print_exc()
        return False


@app.route('/')
def index():
    """Homepage route - displays the main form."""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle prediction requests.
    Supports both single transaction input and CSV file upload.
    """
    global model, quantum_kernel, X_train
    
    if model is None or quantum_kernel is None or X_train is None:
        flash("Model not initialized. Please check server logs.", "error")
        return redirect(url_for('index'))
    
    # Check if CSV file was uploaded
    if 'csv_file' in request.files:
        file = request.files['csv_file']
        if file and file.filename != '':
            return handle_csv_upload(file)
    
    # Handle single transaction prediction
    try:
        v1 = float(request.form.get('v1', 0))
        v2 = float(request.form.get('v2', 0))
        
        prediction, confidence = predict_single(model, quantum_kernel, X_train, v1, v2)
        
        result = {
            'v1': v1,
            'v2': v2,
            'prediction': 'Fraud' if prediction == 1 else 'Not Fraud',
            'prediction_code': prediction,
            'confidence': confidence
        }
        
        return render_template('result.html', result=result, batch_results=None)
    
    except ValueError as e:
        flash(f"Invalid input: {e}. Please enter valid numeric values for V1 and V2.", "error")
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"Error making prediction: {e}", "error")
        return redirect(url_for('index'))


def handle_csv_upload(file):
    """
    Handle CSV file upload for batch predictions.
    
    Args:
        file: Uploaded CSV file (Flask FileStorage object)
    
    Returns:
        Rendered template with batch results
    """
    global model, quantum_kernel, X_train
    
    try:
        # Read CSV file
        df = pd.read_csv(file)
        
        # Check if required columns exist
        if 'V1' not in df.columns or 'V2' not in df.columns:
            flash("CSV file must contain 'V1' and 'V2' columns.", "error")
            return redirect(url_for('index'))
        
        # Extract V1 and V2 features
        X_new = df[['V1', 'V2']].values
        
        # Make predictions
        predictions = predict_batch(model, quantum_kernel, X_train, X_new)
        
        # Prepare results
        results = []
        for i, (idx, row) in enumerate(df.iterrows()):
            results.append({
                'index': i + 1,
                'v1': row['V1'],
                'v2': row['V2'],
                'prediction': 'Fraud' if predictions[i] == 1 else 'Not Fraud',
                'prediction_code': int(predictions[i]),
                # Include other columns if they exist
                'time': row.get('Time', ''),
                'amount': row.get('Amount', ''),
                'class': row.get('Class', '')  # Actual label if present
            })
        
        return render_template('result.html', result=None, batch_results=results)
    
    except Exception as e:
        flash(f"Error processing CSV file: {e}", "error")
        import traceback
        traceback.print_exc()
        return redirect(url_for('index'))


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    API endpoint for programmatic predictions.
    Accepts JSON with 'v1' and 'v2' fields.
    
    Example request:
        {
            "v1": -1.36,
            "v2": -0.073
        }
    
    Returns JSON response with prediction.
    """
    global model, quantum_kernel, X_train
    
    if model is None or quantum_kernel is None or X_train is None:
        return jsonify({'error': 'Model not initialized'}), 500
    
    try:
        data = request.get_json()
        v1 = float(data.get('v1', 0))
        v2 = float(data.get('v2', 0))
        
        prediction, confidence = predict_single(model, quantum_kernel, X_train, v1, v2)
        
        return jsonify({
            'v1': v1,
            'v2': v2,
            'prediction': 'Fraud' if prediction == 1 else 'Not Fraud',
            'prediction_code': int(prediction),
            'confidence': confidence
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    print("Initializing QSVM Fraud Detection Application...")
    print("=" * 50)
    
    # Initialize the model at startup
    if init_model():
        print("=" * 50)
        print("Starting Flask application...")
        
        # Get port from environment variable (Render provides this) or use default 5000
        port = int(os.environ.get('PORT', 5000))
        debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
        
        print(f"Visit http://127.0.0.1:{port} to use the application")
        print("=" * 50)
        
        # Run the Flask application
        # Set debug=False for production (Render), True for local development
        app.run(debug=debug, host='0.0.0.0', port=port)
    else:
        print("Failed to initialize model. Please check the error messages above.")
        print("Make sure creditcard.csv is in the project directory.")


"""
Try neural network approach for health model
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
try:
    from tensorflow import keras
    from tensorflow.keras import layers
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("TensorFlow not available")

from src.data_loader import load_health_data
from pathlib import Path

if TENSORFLOW_AVAILABLE:
    base_path = Path(__file__).parent.parent
    df = load_health_data(str(base_path / "Data" / "wearable_sports_health_dataset.csv"), sample_size=500)
    
    # Simple feature engineering
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Hour'] = df['Timestamp'].dt.hour
    df[['BP_Systolic', 'BP_Diastolic']] = df['Blood_Pressure'].str.split('/', expand=True).astype(float)
    
    le = LabelEncoder()
    y = le.fit_transform(df['Activity_Status'])
    
    # Use most important features based on analysis
    X = df[['Heart_Rate', 'Step_Count', 'Latitude', 'Longitude', 
            'BP_Systolic', 'BP_Diastolic', 'Body_Temperature', 'Blood_Oxygen', 'Hour']].fillna(0)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Create neural network
    model = keras.Sequential([
        layers.Dense(128, activation='relu', input_shape=(X_train_scaled.shape[1],)),
        layers.Dropout(0.3),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(32, activation='relu'),
        layers.Dense(4, activation='softmax')
    ])
    
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    # Train with early stopping
    early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)
    
    history = model.fit(X_train_scaled, y_train, 
                       epochs=200, 
                       batch_size=16,
                       validation_split=0.2,
                       callbacks=[early_stopping],
                       verbose=0)
    
    y_pred = model.predict(X_test_scaled)
    y_pred_classes = np.argmax(y_pred, axis=1)
    
    acc = accuracy_score(y_test, y_pred_classes)
    print(f"Neural Network Accuracy: {acc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_classes, target_names=le.classes_))


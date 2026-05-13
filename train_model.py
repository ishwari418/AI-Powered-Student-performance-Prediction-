import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
import os
import shap

def train_and_evaluate():
    # Load data
    df = pd.read_csv('data/student_data.csv')
    
    # Features and Target
    # We'll predict 'status' (Pass/Fail)
    features = ['attendance', 'study_hours', 'previous_grades', 'parental_education', 
                'internet_access', 'extracurricular_activities', 'sleep_hours', 'assignment_completion']
    X = df[features]
    y = df['status']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'XGBoost': XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    }
    
    results = {}
    best_model = None
    best_f1 = 0
    
    os.makedirs('ml_models', exist_ok=True)
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        results[name] = {
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1_score': f1
        }
        
        print(f"Model: {name}")
        print(f"Accuracy: {acc:.4f}, F1: {f1:.4f}")
        
        if f1 > best_f1:
            best_f1 = f1
            best_model = model
            best_name = name

    # Save Best Model
    model_path = f'ml_models/best_student_model.joblib'
    joblib.dump(best_model, model_path)
    
    # Save SHAP explainer for the best model (if it's tree-based)
    if best_name in ['Random Forest', 'XGBoost']:
        explainer = shap.TreeExplainer(best_model)
        joblib.dump(explainer, 'ml_models/shap_explainer.joblib')
    else:
        # For LR, use KernelExplainer or just LinearExplainer
        explainer = shap.LinearExplainer(best_model, X_train)
        joblib.dump(explainer, 'ml_models/shap_explainer.joblib')
    
    # Save metadata
    metadata = {
        'name': best_name,
        'metrics': results[best_name],
        'features': features
    }
    joblib.dump(metadata, 'ml_models/model_metadata.joblib')
    
    print(f"\nBest Model: {best_name} saved at {model_path}")
    return results

if __name__ == "__main__":
    train_and_evaluate()

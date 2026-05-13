import joblib
import pandas as pd
import numpy as np
import shap
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import PredictionResult, TrainedModel
from apps.students.models import Student, PerformanceRecord

# Load model and metadata at startup
try:
    MODEL = joblib.load('ml_models/best_student_model.joblib')
    METADATA = joblib.load('ml_models/model_metadata.joblib')
    EXPLAINER = joblib.load('ml_models/shap_explainer.joblib')
except:
    MODEL = None
    METADATA = None
    EXPLAINER = None

@login_required
def predict_view(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student = get_object_or_404(Student, student_id=student_id)
        
        # Get latest performance data from form or DB
        data = {
            'attendance': int(request.POST.get('attendance')),
            'study_hours': float(request.POST.get('study_hours')),
            'previous_grades': int(request.POST.get('previous_grades')),
            'parental_education': int(request.POST.get('parental_education')),
            'internet_access': 1 if request.POST.get('internet_access') == 'on' else 0,
            'extracurricular_activities': 1 if request.POST.get('extracurricular_activities') == 'on' else 0,
            'sleep_hours': int(request.POST.get('sleep_hours')),
            'assignment_completion': int(request.POST.get('assignment_completion')),
        }
        
        # Save record
        record = PerformanceRecord.objects.create(
            student=student,
            **data
        )
        
        # Prepare for prediction
        input_df = pd.DataFrame([data])
        
        # Prediction
        prediction = MODEL.predict(input_df)[0]
        prob = MODEL.predict_proba(input_df)[0][prediction]
        
        # SHAP Explanation
        shap_values = EXPLAINER.shap_values(input_df)
        # Handle binary classification SHAP output format
        if isinstance(shap_values, list):
            # For RF in some versions, it returns a list of arrays (one per class)
            current_shap = shap_values[prediction][0]
        else:
            current_shap = shap_values[0]
            
        feature_importance = dict(zip(METADATA['features'], current_shap.tolist()))
        
        # Risk Level
        risk = "Low"
        if prediction == 0:
            risk = "High" if prob > 0.8 else "Medium"
        
        # Recommendations
        recs = []
        if data['attendance'] < 80: recs.append("Improve attendance to at least 85%")
        if data['study_hours'] < 5: recs.append("Increase daily study hours")
        if data['assignment_completion'] < 70: recs.append("Complete all pending assignments")
        if data['sleep_hours'] < 6: recs.append("Ensure at least 7 hours of sleep")
        
        result = PredictionResult.objects.create(
            student=student,
            performance_record=record,
            predicted_score=0.0, # Not used in this version
            predicted_status=prediction,
            confidence_score=float(prob),
            risk_level=risk,
            recommendations=", ".join(recs) if recs else "Keep up the good work!",
            factors_impact=feature_importance
        )
        
        return redirect('prediction_detail', pk=result.pk)

    students = Student.objects.all()
    return render(request, 'predictions/predict_form.html', {'students': students})

class PredictionListView(LoginRequiredMixin, ListView):
    model = PredictionResult
    template_name = 'predictions/prediction_list.html'
    context_object_name = 'predictions'

class PredictionDetailView(LoginRequiredMixin, DetailView):
    model = PredictionResult
    template_name = 'predictions/prediction_detail.html'
    context_object_name = 'result'

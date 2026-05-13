from django.db import models
from apps.students.models import Student, PerformanceRecord

class PredictionResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='predictions')
    performance_record = models.ForeignKey(PerformanceRecord, on_delete=models.CASCADE)
    predicted_score = models.FloatField()
    predicted_status = models.IntegerField(choices=[(0, 'Fail'), (1, 'Pass')])
    confidence_score = models.FloatField()
    risk_level = models.CharField(max_length=20, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    recommendations = models.TextField()
    factors_impact = models.JSONField(help_text="SHAP values or feature importance for this prediction")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction for {self.student.student_id} - {self.risk_level} Risk"

class TrainedModel(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()
    model_file = models.FileField(upload_to='ml_models/')
    is_active = models.BooleanField(default=False)
    trained_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} v{self.version} ({self.accuracy:.2f})"

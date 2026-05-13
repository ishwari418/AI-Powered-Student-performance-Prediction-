from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from apps.students.models import Student, PerformanceRecord
from apps.predictions.models import PredictionResult

@login_required
def dashboard(request):
    total_students = Student.objects.count()
    total_predictions = PredictionResult.objects.count()
    at_risk = PredictionResult.objects.filter(risk_level__in=['High', 'Medium']).count()
    avg_attendance = PerformanceRecord.objects.aggregate(Avg('attendance'))['attendance__avg'] or 0
    
    recent_predictions = PredictionResult.objects.all().order_by('-created_at')[:5]
    
    # Data for charts
    risk_dist = PredictionResult.objects.values('risk_level').annotate(count=Count('risk_level'))
    risk_labels = [d['risk_level'] for d in risk_dist]
    risk_data = [d['count'] for d in risk_dist]
    
    context = {
        'total_students': total_students,
        'total_predictions': total_predictions,
        'at_risk': at_risk,
        'avg_attendance': round(avg_attendance, 2),
        'recent_predictions': recent_predictions,
        'risk_labels': risk_labels,
        'risk_data': risk_data
    }
    return render(request, 'analytics/dashboard.html', context)

@login_required
def analytics_view(request):
    # More detailed analytics
    performance_by_edu = PerformanceRecord.objects.values('parental_education').annotate(avg_score=Avg('exam_score'))
    
    context = {
        'performance_by_edu': performance_by_edu
    }
    return render(request, 'analytics/analytics.html', context)

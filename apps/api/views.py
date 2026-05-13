from rest_framework import viewsets, permissions
from apps.students.models import Student
from apps.predictions.models import PredictionResult
from .serializers import StudentSerializer, PredictionSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

class PredictionViewSet(viewsets.ModelViewSet):
    queryset = PredictionResult.objects.all()
    serializer_class = PredictionSerializer
    permission_classes = [permissions.IsAuthenticated]

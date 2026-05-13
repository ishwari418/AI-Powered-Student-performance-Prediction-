from rest_framework import serializers
from apps.students.models import Student
from apps.predictions.models import PredictionResult

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionResult
        fields = '__all__'

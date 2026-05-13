from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

class PerformanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='performance_records')
    attendance = models.IntegerField(help_text="Attendance percentage (0-100)")
    study_hours = models.FloatField(help_text="Average study hours per day")
    previous_grades = models.IntegerField(help_text="Previous exam score (0-100)")
    parental_education = models.IntegerField(choices=[(0, 'None'), (1, 'High School'), (2, 'Bachelor'), (3, 'Master+')], default=1)
    internet_access = models.BooleanField(default=True)
    extracurricular_activities = models.BooleanField(default=False)
    sleep_hours = models.IntegerField(default=7)
    assignment_completion = models.IntegerField(help_text="Assignment completion percentage (0-100)")
    exam_score = models.IntegerField(null=True, blank=True, help_text="Actual exam score (if available)")
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record for {self.student.student_id} at {self.recorded_at.date()}"

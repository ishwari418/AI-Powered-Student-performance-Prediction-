import csv
import io
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Student, PerformanceRecord

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Student.objects.filter(student_id__icontains=query) | Student.objects.filter(first_name__icontains=query)
        return Student.objects.all()

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    fields = ['student_id', 'first_name', 'last_name', 'email', 'department']
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        messages.success(self.request, "Student added successfully!")
        return super().form_valid(form)

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    fields = ['first_name', 'last_name', 'email', 'department']
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')

def upload_csv(request):
    if request.method == "POST":
        csv_file = request.FILES.get('file')
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file')
            return redirect('upload_csv')
        
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string) # Skip header
        
        count = 0
        for row in csv.reader(io_string, delimiter=',', quotechar='|'):
            # student_id, attendance, study_hours, previous_grades, parental_education, internet_access, extracurricular_activities, sleep_hours, assignment_completion, exam_score, status, grade_category
            _, created = Student.objects.update_or_create(
                student_id=row[0],
                defaults={
                    'first_name': f"Student",
                    'last_name': row[0],
                    'email': f"student{row[0]}@example.com"
                }
            )
            
            student_obj = Student.objects.get(student_id=row[0])
            
            PerformanceRecord.objects.create(
                student=student_obj,
                attendance=int(row[1]),
                study_hours=float(row[2]),
                previous_grades=int(row[3]),
                parental_education=int(row[4]),
                internet_access=bool(int(row[5])),
                extracurricular_activities=bool(int(row[6])),
                sleep_hours=int(row[7]),
                assignment_completion=int(row[8]),
                exam_score=int(row[9])
            )
            count += 1
        
        messages.success(request, f"Successfully uploaded {count} student records!")
        return redirect('student_list')

    return render(request, 'students/upload.html')

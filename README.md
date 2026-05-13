# EduPredict AI: Student Performance Prediction & Academic Intervention System

EduPredict AI is a sophisticated full-stack educational analytics platform designed to predict student academic performance and provide early interventions using Machine Learning.

## Features

- **AI-Powered Predictions**: Predicts pass/fail status and risk levels with high accuracy using Random Forest and XGBoost.
- **Explainable AI (XAI)**: Integrated SHAP (SHapley Additive exPlanations) to visualize exactly which factors (attendance, study hours, etc.) influenced each prediction.
- **Academic Dashboard**: Real-time analytics on student risk distribution, attendance trends, and performance metrics.
- **Student Management**: Full CRUD for student records and bulk data import via CSV.
- **Intervention Engine**: Generates personalized academic recommendations for at-risk students.
- **REST API Support**: Built-in endpoints for integration with other educational tools.
- **Modern UI**: Clean, responsive dashboard built with Bootstrap 5 and Chart.js.

## Tech Stack

- **Backend**: Django, Django REST Framework
- **ML Engine**: Scikit-learn, XGBoost, Pandas, NumPy
- **Explainability**: SHAP
- **Frontend**: HTML5, Vanilla CSS, Bootstrap 5, JavaScript, Chart.js
- **Database**: SQLite (PostgreSQL compatible)

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Generate Synthetic Data & Train Model**:
   ```bash
   python generate_data.py
   python train_model.py
   ```

4. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Start Server**:
   ```bash
   python manage.py runserver
   ```

## Usage

1. Login as Admin.
2. Navigate to **Upload Data** and upload the generated `data/student_data.csv`.
3. Go to **Predictions** to run AI assessments on specific students.
4. View the **Dashboard** for overall academic health metrics.

---
Developed for professional placement portfolios.

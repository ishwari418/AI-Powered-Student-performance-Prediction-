import pandas as pd
import numpy as np
import os

def generate_student_data(n=1000):
    np.random.seed(42)
    
    data = {
        'student_id': range(1, n + 1),
        'attendance': np.random.randint(60, 100, n),
        'study_hours': np.random.randint(1, 15, n),
        'previous_grades': np.random.randint(40, 100, n),
        'parental_education': np.random.choice([0, 1, 2, 3], n), # 0: None, 1: High School, 2: Bachelor, 3: Master+
        'internet_access': np.random.choice([0, 1], n),
        'extracurricular_activities': np.random.choice([0, 1], n),
        'sleep_hours': np.random.randint(4, 10, n),
        'assignment_completion': np.random.randint(50, 100, n),
    }
    
    df = pd.DataFrame(data)
    
    # Generate Target: Exam Score based on features
    # Base score
    score = (
        df['attendance'] * 0.3 +
        df['study_hours'] * 2.0 +
        df['previous_grades'] * 0.4 +
        df['parental_education'] * 2.0 +
        df['assignment_completion'] * 0.2 +
        np.random.normal(0, 5, n) # Noise
    )
    
    # Normalize score to 0-100
    df['exam_score'] = np.clip(score, 0, 100).astype(int)
    
    # Pass/Fail (Pass if exam_score >= 50)
    df['status'] = (df['exam_score'] >= 50).astype(int)
    
    # Grade Category
    def get_grade(s):
        if s >= 90: return 'A'
        if s >= 80: return 'B'
        if s >= 70: return 'C'
        if s >= 60: return 'D'
        return 'F'
    
    df['grade_category'] = df['exam_score'].apply(get_grade)
    
    return df

if __name__ == "__main__":
    df = generate_student_data(1000)
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/student_data.csv', index=False)
    print("Synthetic dataset generated at data/student_data.csv")

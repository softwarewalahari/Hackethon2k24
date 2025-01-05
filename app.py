from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import HistGradientBoostingRegressor

app = Flask(__name__)

# Load data (you can load data dynamically if required)
data = pd.read_csv('student_dataset.csv')

# Feature engineering function
def process_data():
    data['avg_gpa'] = data['Cumulative GPA']
    data['core_course_score'] = data['Core Engineering Course Grades'].apply(lambda x: sum([4 if grade=='A' else 3 if grade=='B' else 2 if grade=='C' else 1 if grade=='D' else 0 for grade in x.split(',')]) / 5)
    data['hackathon_score'] = data['Hackathon Participation'].map({'International': 3, 'National': 2, 'Local': 1, 'None': 0})
    data['paper_count'] = data['Paper Presentations']
    data['research_count'] = data['Research Publications']
    data['leadership_score'] = data['Leadership Roles'].map({'President': 3, 'Vice President': 2, 'Treasurer': 1, 'None': 0})

    numerical_features = ['avg_gpa', 'core_course_score', 'hackathon_score', 'paper_count', 'research_count', 'leadership_score', 'Certifications', 'Workshops Attended', 'Internships', 'Attendance Record', 'Scholarships/Awards']

    # Impute missing values
    imputer = SimpleImputer(strategy='mean')
    data[numerical_features] = imputer.fit_transform(data[numerical_features])

    # Normalize numerical features
    scaler = StandardScaler()
    data[numerical_features] = scaler.fit_transform(data[numerical_features])

    # Train model
    X = data[numerical_features]
    y = data['Cumulative GPA']

    model = HistGradientBoostingRegressor()
    model.fit(X, y)

    # Score students
    data['score'] = model.predict(X)

    # Rank students by year
    def get_top_3(group):
        return group.nlargest(3, 'score')

    top_students = data.groupby('Year').apply(get_top_3).reset_index(drop=True)
    return top_students

# Route to display top students
@app.route('/')
def display_top_students():
    top_students = process_data()
    return render_template('web/top_students.html', top_students=top_students)

if __name__ == "__main__":
    app.run(debug=True)

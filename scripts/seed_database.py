import json
import os
import sys

# Add parent directory to path so we can import from database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import db
from database.models import User, Experiment, Badge
from app import create_app

def seed_db():
    app = create_app()
    with app.app_context():
        # Clean current
        db.drop_all()
        db.create_all()

        # Add Teacher
        teacher = User(name="Admin Teacher", email="teacher@lab.edu", role="teacher")
        teacher.set_password("teacher123")
        db.session.add(teacher)

        # Add Student
        student = User(name="Test Student", email="student@lab.edu", role="student")
        student.set_password("student123")
        db.session.add(student)

        db.session.add(student)

        # Add Initial Badges
        badges = [
            Badge(name="First Blood", description="Completed the first experiment.", icon="bi-award"),
            Badge(name="Arduino Master", description="Completed 5 Arduino experiments.", icon="bi-cpu"),
            Badge(name="Pi Explorer", description="Completed 3 Raspberry Pi experiments.", icon="bi-motherboard")
        ]
        db.session.add_all(badges)

        db.session.commit()

        # Load experiments from files
        exp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'experiments')
        for platform_type in ['arduino', 'raspberry_pi']:
            folder_path = os.path.join(exp_dir, platform_type)
            if os.path.exists(folder_path):
                for filename in os.listdir(folder_path):
                    if filename.endswith(".json"):
                        with open(os.path.join(folder_path, filename), 'r') as f:
                            data = json.load(f)
                            exp = Experiment(
                                title=data['title'],
                                description=data['description'],
                                type=data['type'],
                                difficulty=data.get('difficulty', 'easy'),
                                category=data.get('category', 'General'),
                                wokwi_url=data['wokwi_url']
                            )
                            db.session.add(exp)
        
        db.session.commit()
        print("Database seeded with Test Users and initial Experiments!")

if __name__ == "__main__":
    seed_db()

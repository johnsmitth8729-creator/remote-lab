from app import create_app, db
from app.models import User, Experiment, Badge
import random

app = create_app()

def seed():
    with app.app_context():
        # Clear existing
        db.drop_all()
        db.create_all()

        # Create Users
        admin = User(name="Admin Teacher", email="admin@lab.com", role="teacher")
        admin.set_password("admin123")
        
        student = User(name="John Doe", email="student@lab.com", role="student")
        student.set_password("student123")
        
        db.session.add_all([admin, student])

        # Create Experiments
        experiments = [
            # Arduino
            {
                "title": "LED Blink",
                "description": "The 'Hello World' of electronics. Learn how to blink an LED using Arduino.",
                "type": "arduino",
                "difficulty": "easy",
                "wokwi_url": "https://wokwi.com/projects/arduino-blink",
                "category": "Basic Electronics"
            },
            {
                "title": "Button Controlled LED",
                "description": "Use a push button to turn an LED on and off.",
                "type": "arduino",
                "difficulty": "easy",
                "wokwi_url": "https://wokwi.com/projects/305214041180242496",
                "category": "Digital Input"
            },
            {
                "title": "Traffic Light System",
                "description": "Simulate a real-world traffic light timing sequence.",
                "type": "arduino",
                "difficulty": "medium",
                "wokwi_url": "https://wokwi.com/projects/311545638162235968",
                "category": "Control Logic"
            },
            {
                "title": "Temperature Sensor DHT11",
                "description": "Read temperature and humidity values from a DHT11 sensor.",
                "type": "arduino",
                "difficulty": "medium",
                "wokwi_url": "https://wokwi.com/projects/322850130954551890",
                "category": "Sensors"
            },
            {
                "title": "Ultrasonic Distance Sensor",
                "description": "Measure distance using HC-SR04 ultrasonic sensor and display on Serial.",
                "type": "arduino",
                "difficulty": "hard",
                "wokwi_url": "https://wokwi.com/projects/299411986423546378",
                "category": "Sensors"
            },
            # Raspberry Pi Pico
            {
                "title": "LED Control using MicroPython",
                "description": "Learn basic MicroPython by controlling an LED on Raspberry Pi Pico.",
                "type": "raspberry_pi_pico",
                "difficulty": "easy",
                "wokwi_url": "https://wokwi.com/projects/305214041180242496", # Placeholder
                "category": "MicroPython"
            },
            {
                "title": "Temperature Monitoring System",
                "description": "Build a system that monitors environmental temperature using Pico.",
                "type": "raspberry_pi_pico",
                "difficulty": "medium",
                "wokwi_url": "https://wokwi.com/projects/322850130954551890", # Placeholder
                "category": "IoT"
            },
            {
                "title": "Light Sensor System",
                "description": "Detect light levels and respond using a photoresistor on Pico.",
                "type": "raspberry_pi_pico",
                "difficulty": "medium",
                "wokwi_url": "https://wokwi.com/projects/299411986423546378", # Placeholder
                "category": "Sensors"
            }
        ]

        for exp_data in experiments:
            exp = Experiment(**exp_data)
            db.session.add(exp)

        # Create Badges
        badges = [
            Badge(name="First Success", description="Completed your first experiment", icon="bi-award", points_required=0),
            Badge(name="Arduino Master", description="Completed 5 Arduino experiments", icon="bi-cpu", points_required=50),
            Badge(name="Pi Explorer", description="Completed 3 Raspberry Pi Pico experiments", icon="bi-raspberry-pi", points_required=30)
        ]
        db.session.add_all(badges)

        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed()

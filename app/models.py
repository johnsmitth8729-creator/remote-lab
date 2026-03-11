from .extensions import db, bcrypt
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='student')  # student / teacher
    points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    submissions = db.relationship('Submission', backref='student', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "points": self.points,
            "created_at": self.created_at.isoformat()
        }

class Experiment(db.Model):
    __tablename__ = 'experiments'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    objectives = db.Column(db.Text, nullable=True)
    instructions = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(50), nullable=False)  # arduino / raspberry_pi_pico
    difficulty = db.Column(db.String(20), default='easy') # easy, medium, hard
    category = db.Column(db.String(100), nullable=True)
    wokwi_url = db.Column(db.String(500), nullable=False)
    expected_result = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    submissions = db.relationship('Submission', backref='experiment', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "objectives": self.objectives,
            "instructions": self.instructions,
            "type": self.type,
            "difficulty": self.difficulty,
            "category": self.category,
            "wokwi_url": self.wokwi_url,
            "expected_result": self.expected_result,
            "created_at": self.created_at.isoformat()
        }

class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiments.id'), nullable=False)
    result_text = db.Column(db.Text, nullable=True)
    score = db.Column(db.Integer, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "experiment_id": self.experiment_id,
            "result_text": self.result_text,
            "score": self.score,
            "feedback": self.feedback,
            "submitted_at": self.submitted_at.isoformat()
        }

class Badge(db.Model):
    __tablename__ = 'badges'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    points_required = db.Column(db.Integer, default=0)

class UserBadge(db.Model):
    __tablename__ = 'user_badges'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badges.id'), nullable=False)
    awarded_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('badges_awarded', lazy=True))
    badge = db.relationship('Badge', backref=db.backref('users_awarded', lazy=True))

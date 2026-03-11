from database.models import User
from database.db import db

class UserService:

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_identifier(identifier):
        # Try finding by email first, otherwise fallback to name searching
        user = User.query.filter_by(email=identifier).first()
        if not user:
            user = User.query.filter_by(name=identifier).first()
        return user

    @staticmethod
    def get_all_students():
        return User.query.filter_by(role='student').all()

    @staticmethod
    def create_user(name, email, password, role='student'):
        if UserService.get_user_by_email(email):
            return None # Email already exists
            
        user = User(name=name, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

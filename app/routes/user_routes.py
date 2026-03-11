from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User, Submission, Experiment
from ..extensions import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    recent_submissions = Submission.query.filter_by(user_id=user_id)\
        .order_by(Submission.submitted_at.desc()).limit(5).all()
    
    stats = {
        "completed": Submission.query.filter_by(user_id=user_id).count(),
        "points": user.points,
        "rank": "Novice" # Placeholder for rank logic
    }
    
    available_experiments = Experiment.query.limit(3).all()
    
    leaderboard = User.query.filter_by(role='student').order_by(User.points.desc()).limit(5).all()
    
    return render_template('dashboard/student.html', 
                           user=user, 
                           submissions=recent_submissions,
                           stats=stats,
                           available_experiments=available_experiments,
                           leaderboard=leaderboard)

@user_bp.route('/profile')
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return render_template('dashboard/profile.html', user=user)

@user_bp.route('/submissions')
@jwt_required()
def submissions():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    all_submissions = Submission.query.filter_by(user_id=user_id)\
        .order_by(Submission.submitted_at.desc()).all()
    return render_template('dashboard/submissions.html', user=user, submissions=all_submissions)

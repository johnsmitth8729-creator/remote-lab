from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..models import Experiment, Submission, User
from ..extensions import db

experiment_bp = Blueprint('experiment', __name__)

@experiment_bp.route('/')
@jwt_required(optional=True)
def list_experiments():
    search = request.args.get('search')
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    
    query = Experiment.query
    if search:
        query = query.filter(Experiment.title.contains(search))
    if category:
        query = query.filter_by(category=category)
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
        
    experiments = query.all()
    categories = db.session.query(Experiment.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    
    return render_template('experiments/list.html', 
                           experiments=experiments, 
                           categories=categories)

@experiment_bp.route('/<int:id>')
@jwt_required()
def detail(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        flash('Sessiya muddati tugagan yoki foydalanuvchi topilmadi. Iltimos, qayta kiring.', 'warning')
        return redirect(url_for('auth.login'))
        
    experiment = Experiment.query.get_or_404(id)
    # Get latest submission for this user and experiment
    last_submission = Submission.query.filter_by(user_id=user_id, experiment_id=id)\
        .order_by(Submission.submitted_at.desc()).first()
    return render_template('experiments/detail.html', 
                           experiment=experiment, 
                           last_submission=last_submission)

@experiment_bp.route('/<int:id>/submit', methods=['POST'])
@jwt_required()
def submit(id):
    user_id = get_jwt_identity()
    result_text = request.form.get('result_text')
    
    submission = Submission(
        user_id=user_id,
        experiment_id=id,
        result_text=result_text,
        score=10 # Auto-graded for now
    )
    db.session.add(submission)
    
    # Simple auto-points for now
    user = User.query.get(user_id)
    if not user:
        flash('Sessiya muddati tugagan yoki foydalanuvchi topilmadi. Iltimos, qayta kiring.', 'warning')
        return redirect(url_for('auth.login'))
        
    user.points += 10
    
    db.session.commit()
    flash('Experiment result submitted successfully! +10 points earned.', 'success')
    return redirect(url_for('experiment.detail', id=id))

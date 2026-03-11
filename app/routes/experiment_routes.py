from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..models import Experiment, Submission, User
from ..extensions import db

experiment_bp = Blueprint('experiment', __name__)

@experiment_bp.route('/')
@jwt_required()
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
    experiment = Experiment.query.get_or_404(id)
    return render_template('experiments/detail.html', experiment=experiment)

@experiment_bp.route('/<int:id>/submit', methods=['POST'])
@jwt_required()
def submit(id):
    user_id = get_jwt_identity()
    result_text = request.form.get('result_text')
    
    submission = Submission(
        user_id=user_id,
        experiment_id=id,
        result_text=result_text
    )
    db.session.add(submission)
    
    # Simple auto-points for now
    user = User.query.get(user_id)
    user.points += 10
    
    db.session.commit()
    flash('Experiment result submitted successfully! +10 points earned.', 'success')
    return redirect(url_for('experiment.detail', id=id))

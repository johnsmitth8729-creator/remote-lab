from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt
from ..models import Experiment, Submission, User
from ..extensions import db

admin_bp = Blueprint('admin', __name__)

def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get('role') != 'teacher':
            flash('Admin access required.', 'danger')
            return redirect(url_for('user.dashboard'))
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    total_students = User.query.filter_by(role='student').count()
    total_experiments = Experiment.query.count()
    total_submissions = Submission.query.count()
    
    recent_submissions = Submission.query.order_by(Submission.submitted_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html', 
                           stats={
                               "students": total_students,
                               "experiments": total_experiments,
                               "submissions": total_submissions
                           },
                           submissions=recent_submissions)

@admin_bp.route('/experiments/new', methods=['GET', 'POST'])
@admin_required
def create_experiment():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        wokwi_url = request.form.get('wokwi_url')
        exp_type = request.form.get('type')
        difficulty = request.form.get('difficulty')
        
        new_exp = Experiment(
            title=title,
            description=description,
            wokwi_url=wokwi_url,
            type=exp_type,
            difficulty=difficulty
        )
        db.session.add(new_exp)
        db.session.commit()
        flash('Experiment created successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('admin/experiment_form.html')

@admin_bp.route('/experiments/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_experiment(id):
    experiment = Experiment.query.get_or_404(id)
    if request.method == 'POST':
        experiment.title = request.form.get('title')
        experiment.description = request.form.get('description')
        experiment.instructions = request.form.get('instructions')
        experiment.wokwi_url = request.form.get('wokwi_url')
        experiment.type = request.form.get('type')
        experiment.difficulty = request.form.get('difficulty')
        experiment.category = request.form.get('category')
        
        db.session.commit()
        flash('Experiment updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('admin/experiment_form.html', experiment=experiment)

@admin_bp.route('/experiments/<int:id>/delete', methods=['POST'])
@admin_required
def delete_experiment(id):
    experiment = Experiment.query.get_or_404(id)
    db.session.delete(experiment)
    db.session.commit()
    flash('Experiment deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/submission/<int:id>/grade', methods=['POST'])
@admin_required
def grade_submission(id):
    submission = Submission.query.get_or_404(id)
    score = request.form.get('score')
    feedback = request.form.get('feedback')
    
    submission.score = int(score)
    submission.feedback = feedback
    
    # Update student points
    student = User.query.get(submission.user_id)
    student.points += int(score)
    
    db.session.commit()
    flash('Submission graded successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

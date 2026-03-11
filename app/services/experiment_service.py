from database.db import db
from database.models import Experiment, Submission

class ExperimentService:

    @staticmethod
    def get_all_experiments():
        return Experiment.query.all()

    @staticmethod
    def get_experiment(experiment_id):
        return Experiment.query.get(experiment_id)

    @staticmethod
    def create_experiment(title, description, exp_type, wokwi_url):
        exp = Experiment(title=title, description=description, type=exp_type, wokwi_url=wokwi_url)
        db.session.add(exp)
        db.session.commit()
        return exp

    @staticmethod
    def delete_experiment(experiment_id):
        exp = Experiment.query.get(experiment_id)
        if exp:
            db.session.delete(exp)
            db.session.commit()
            return True
        return False
        
    @staticmethod
    def submit_experiment(student_id, experiment_id, notes=None):
        # Prevent duplicate submissions
        existing = Submission.query.filter_by(student_id=student_id, experiment_id=experiment_id).first()
        if existing:
            return existing

        submission = Submission(student_id=student_id, experiment_id=experiment_id, notes=notes)
        db.session.add(submission)
        db.session.commit()
        return submission

    @staticmethod
    def get_student_submissions(student_id):
        return Submission.query.filter_by(student_id=student_id).all()
        
    @staticmethod
    def get_all_submissions():
        return Submission.query.all()

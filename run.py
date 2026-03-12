from app import create_app, db
from app.models import User, Experiment, Submission, Badge
import os
import logging

app = create_app()

# Attempt to create tables on startup — wrapped so a DB connection issue
# doesn't prevent gunicorn from binding to the port on Render.
with app.app_context():
    try:
        db.create_all()
        logging.info("Database tables created/verified successfully.")
    except Exception as e:
        logging.error(f"Could not create database tables at startup: {e}")

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Experiment': Experiment, 'Submission': Submission, 'Badge': Badge}

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


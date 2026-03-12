from app import create_app, db
from app.models import User, Experiment, Submission, Badge
import os

app = create_app()

with app.app_context():
    db.create_all()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Experiment': Experiment, 'Submission': Submission, 'Badge': Badge}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


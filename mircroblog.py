# Python script at the top-level that defines the Flask application instance
from app import app, db
from app.models import User, Post


@app.shell_context_processor
def make_shell_context():
    shell_instances = {'db': db, 'User': User, 'Post': Post}
    return shell_instances

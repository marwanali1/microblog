from app import app


@app.route('/')
@app.route('/index')
def index():
    """
    View function with route URL decorators
    """
    return "Hello, World!"

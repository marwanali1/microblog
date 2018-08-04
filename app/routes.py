from app import app


@app.route('/')
@app.route('/index')
def index():
    """
    View function with route URL decorators
    """
    user = {'username': 'Marwan'}
    html_str = '''
    <html>
        <head>
            <title>Home Page - Microblog</title>
        </head>
        <body>
            <h1>Hello, ''' + user['username'] + '''!</h1>
        </body>
    </html>
    '''
    return html_str

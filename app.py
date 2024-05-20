from flask import Flask, url_for, request
from markupsafe import escape

app = Flask(__name__)

# Static routes
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def test():
    return "<p><strong>Testing page - secondary route</strong></p>"

# Dynamic routes
@app.route("/profile/<username>")
def profile(username):
    return f"<p><strong>Hello, {escape(username)}!</strong></p>"

@app.route("/post/<int:post_id>")
def post_index(post_id):
    return f"Post {post_id}"

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return f'Posting login creds...'
    else:
        return f'Logged in! Redirecting to about page.'

with app.test_request_context():
    print(url_for('post_index', post_id=7))
    print(url_for('projects'))
    print(url_for('login'))
    print(url_for('login', next='/about'))
    print(url_for('profile', username='Rick Sanchez'))
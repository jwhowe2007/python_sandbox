from flask import Flask, url_for, request, render_template
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
    return render_template('about.html')

@app.get("/login")
def login_get():
    return f'Logged in! Redirecting to the About page.'

@app.post("/login")
def login_post():
    return f'Posting login creds...'

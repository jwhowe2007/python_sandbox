from flask import Flask, url_for, request, render_template
from markupsafe import Markup, escape

app = Flask(__name__)

# Static routes
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def test():
    return render_template('test.html')

# Dynamic routes
@app.route("/profile/")
@app.route("/profile/<username>")
def profile(username=None):
    return render_template('profile.html', name=escape(username))

@app.route("/post/<int:post_id>")
def post_index(post_id):
    return f"Post {post_id}"

@app.route('/about')
def about():
    return render_template('about.html')

@app.get("/login")
def login_get():
    return f'Logged in! Redirecting to the About page.'

@app.post("/login")
def login_post():
    return f'Posting login creds...'

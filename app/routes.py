from flask import Blueprint, redirect, render_template_string, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from . import db
from .models import User


main = Blueprint("main", __name__)


HOME_TEMPLATE = """
<h1>Security Study Tracker</h1>

{% if current_user.is_authenticated %}
    <p>You are logged in as {{ current_user.username }}.</p>
    <p><a href="{{ url_for('main.dashboard') }}">Dashboard</a></p>
    <p><a href="{{ url_for('main.logout') }}">Logout</a></p>
{% else %}
    <p>You are not logged in.</p>
    <p><a href="{{ url_for('main.register') }}">Register</a></p>
    <p><a href="{{ url_for('main.login') }}">Login</a></p>
{% endif %}
"""


REGISTER_TEMPLATE = """
<h1>Register</h1>

<form method="post">
    <label>Username</label>
    <input name="username" required>

    <label>Password</label>
    <input name="password" type="password" required>

    <button type="submit">Register</button>
</form>

<p>{{ message }}</p>
<p><a href="{{ url_for('main.home') }}">Home</a></p>
"""


LOGIN_TEMPLATE = """
<h1>Login</h1>

<form method="post">
    <label>Username</label>
    <input name="username" required>

    <label>Password</label>
    <input name="password" type="password" required>

    <button type="submit">Login</button>
</form>

<p>{{ message }}</p>
<p><a href="{{ url_for('main.home') }}">Home</a></p>
"""


DASHBOARD_TEMPLATE = """
<h1>Dashboard</h1>

<p>Welcome, {{ current_user.username }}.</p>
<p>This is a protected page.</p>
<p><a href="{{ url_for('main.logout') }}">Logout</a></p>
"""


@main.route("/")
def home():
    return render_template_string(HOME_TEMPLATE)


@main.route("/health")
def health():
    return {"status": "ok"}


@main.route("/register", methods=["GET", "POST"])
def register():
    message = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            message = "Username and password are required."
            return render_template_string(REGISTER_TEMPLATE, message=message)

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            message = "Username already exists."
            return render_template_string(REGISTER_TEMPLATE, message=message)

        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("main.login"))

    return render_template_string(REGISTER_TEMPLATE, message=message)


@main.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("main.dashboard"))

        message = "Invalid username or password."

    return render_template_string(LOGIN_TEMPLATE, message=message)


@main.route("/dashboard")
@login_required
def dashboard():
    return render_template_string(DASHBOARD_TEMPLATE)


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))

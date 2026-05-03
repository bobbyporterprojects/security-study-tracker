from flask import Blueprint

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return "Security Study Tracker is running!"


@main.route("/health")
def health():
    return {"status": "ok"}

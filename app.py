from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

topics = [
    {"name": "Threats, Attacks, and Vulnerabilities", "complete": False},
    {"name": "Architecture and Design", "complete": False},
    {"name": "Implementation", "complete": False},
    {"name": "Operations and Incident Response", "complete": False},
    {"name": "Governance, Risk, and Compliance", "complete": False},
]


@app.route("/")
def index():
    completed = sum(1 for topic in topics if topic["complete"])
    total = len(topics)
    percent = int((completed / total) * 100)

    app_env = os.getenv("APP_ENV", "development")

    return render_template(
        "index.html",
        topics=topics,
        completed=completed,
        total=total,
        percent=percent,
        app_env=app_env,
    )


@app.route("/toggle/<int:topic_id>", methods=["POST"])
def toggle_topic(topic_id):
    if 0 <= topic_id < len(topics):
        topics[topic_id]["complete"] = not topics[topic_id]["complete"]

    return redirect(url_for("index"))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

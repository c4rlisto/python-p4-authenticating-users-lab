#!/usr/bin/env python3

from flask import Flask, request, session, jsonify
from flask_migrate import Migrate
from models import db, User

# --------------------
# App Setup
# --------------------

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "super-secret-key"

# --------------------
# Initialize Extensions
# --------------------

db.init_app(app)
migrate = Migrate(app, db)

# --------------------
# Routes
# --------------------

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    session["user_id"] = user.id
    return jsonify(user.to_dict()), 200


@app.route("/logout", methods=["DELETE"])
def logout():
    session.pop("user_id", None)
    return {}, 204


@app.route("/check_session", methods=["GET"])
def check_session():
    user_id = session.get("user_id")

    if user_id:
        user = User.query.get(user_id)
        if user:
            return jsonify(user.to_dict()), 200

    return {}, 401


# REQUIRED BY TESTS
@app.route("/clear")
def clear():
    session.clear()
    return {}, 204


# --------------------
# Run App
# --------------------

if __name__ == "__main__":
    app.run(port=5555, debug=True)

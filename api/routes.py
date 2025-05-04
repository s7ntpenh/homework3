from flask import jsonify, Blueprint, render_template

from database import db
from  models.sqlalchemy.student import Student
bp = Blueprint("main_bp", __name__, url_prefix="/")

@bp.route('/')
def home() -> str:
    return render_template('home_page.html')

@bp.route("/test", methods=["DELETE"])
def route_test():
    db.session.get(Student, 1)
    return jsonify({"message": "Hello"}), 200

@bp.route("/new-test")
def route_test_2():
    return jsonify({"message": "Hello 2"}), 200

@bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200




from flask import Blueprint, jsonify, request

from database import db
from models.pydantic.students.student_read import StudentReadModel
from models.pydantic.students.student_update import StudentUpdateModel
from models.pydantic.students.student_create import StudentCreateModel
from models.sqlalchemy.student import Student

students_bp = Blueprint("students_bp", __name__, url_prefix="/students")


@students_bp.route("/", methods=["GET"])
def get_all_students():
    name_filter = request.args.get("name", type=str)
    q = Student.query
    if name_filter:
        q = q.filter(Student.name.ilike(f"%{name_filter}%"))
    students = q.all()

    result = [
        StudentReadModel.model_validate(s).model_dump(mode="json")
        for s in students
    ]
    return jsonify({"students": result}), 200

@students_bp.route('/', methods=['POST'])
def create_student():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    student_in = StudentCreateModel.model_validate(data)
    new_student = Student(**student_in.model_dump())
    db.session.add(new_student)
    db.session.commit()

    return jsonify(StudentReadModel.model_validate(new_student).model_dump(mode='json')), 201
    

@students_bp.route("/<int:pk>", methods=["GET"])
def get_student_by_id(pk):
    student = Student.query.get(pk)
    if student is None:
        return jsonify({"error": f"Student with id={pk} not found"}), 404

    return jsonify(StudentReadModel.model_validate(student).model_dump(mode="json"))



@students_bp.route("/<int:pk>", methods=["DELETE"])
def delete_student_by_id(pk):
    student = Student.query.get(pk)
    if student is None:
        return jsonify({"error": f"Student with id={pk} not found"}), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({"message": "Student was successfully deleted"}), 204


@students_bp.route("/<int:pk>", methods=["PATCH"])
def edit_student_by_id(pk):
    student = Student.query.get(pk)
    if student is None:
        return jsonify({"error": f"Student with id={pk} not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": f"No data provided"}), 400

    validated_data = StudentUpdateModel.model_validate(data)
    for field, value in validated_data.model_dump(exclude_none=True).items():
        if value is not None:
            setattr(student, field, value)
    db.session.commit()


    return jsonify(StudentReadModel.model_validate(student).model_dump(mode="json"))


@students_bp.route("/", methods=["POST"])
def create_student_by_id():

    data = request.get_json()
    if not data:
        return jsonify({"error": f"No data provided"}), 400

    validated_data = StudentUpdateModel.model_validate(data)
    new_student = Student(**validated_data.model_dump())

    db.session.add(new_student)
    db.session.commit()


    return jsonify(StudentReadModel.model_validate(new_student).model_dump(mode="json")), 201
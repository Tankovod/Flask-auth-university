import datetime

from flask import render_template, request, Blueprint
from flask_login import login_required

from ..database.simple_models import Student, University, db


view = Blueprint("view", __name__)


@view.route("/", methods=["GET"])
def index():
    return render_template('university/index.html')


@view.route("/university/about", methods=["GET"])
def about():
    return render_template('university/about.html')


@view.route("/universities", methods=["GET"])
def universities():
    unis_ = University.query.all()
    return render_template('university/universities.html', **{'universities': unis_})


@view.route("/university-update/<uni_id>", methods=["GET", "POST"])
@login_required
def update_uni(uni_id):
    uni_ = University.query.filter(University.id == uni_id).first()
    if request.method == "POST":
        uni_.full_name = request.form.get("full_name")
        uni_.short_name = request.form.get("short_name")
        uni_.created_at = datetime.datetime.fromisoformat(request.form.get("created_at"))
        db.session.add(uni_)
        db.session.commit()
        db.session.refresh(uni_)
        return render_template('university/update_university.html', **{"form": uni_})

    return render_template('university/update_university.html', **{"form": uni_})


@view.route("/university-delete/<uni_id>", methods=["GET", "POST"])
def delete_uni(uni_id):
    uni_ = University.query.filter(University.id == uni_id).first()
    if request.method == "POST":
        db.session.delete(uni_)
        db.session.commit()
        unis_ = University.query.all()
        return render_template('university/universities.html', **{'universities': unis_})
    return render_template('university/delete_university.html', **{"university": uni_})


@view.route("/university-detail/<uni_id>", methods=["GET"])
def uni_info(uni_id):
    uni_ = University.query.filter(University.id == uni_id).first()
    return render_template('university/university_detail_view.html', **{'university': uni_})


@view.route("/student-update/<stu_id>", methods=["GET", "POST"])
@login_required
def update_stu(stu_id):
    s = Student.query.filter(Student.id == stu_id).first()
    universities_ = University.query.all()

    if request.method == "POST":
        s.full_name = request.form.get("full_name")
        s.university_id = request.form.get("university_id")
        s.year_of_admission = request.form.get("year_of_admission")
        s.date_of_birth = datetime.datetime.fromisoformat(request.form.get("date_of_birth"))
        db.session.add(s)
        db.session.commit()
        db.session.refresh(s)
        return render_template('university/update_student.html', **{"form": s}, **{"universities": universities_})
    return render_template('university/update_student.html', **{"form": s}, **{"universities": universities_})


@view.route("/student-delete/<stu_id>", methods=["GET", "POST"])
def delete_stu(stu_id):
    s = Student.query.filter(Student.id == stu_id).first()
    if request.method == "POST":
        db.session.delete(s)
        db.session.commit()
        st_ = Student.query.all()
        return render_template('university/students.html', **{'students': st_})

    return render_template('university/delete_student.html', **{"student": s})


@view.route("/student-detail/<stu_id>", methods=["GET"])
def stu_info(stu_id):
    s = Student.query.filter(Student.id == stu_id).first()
    return render_template('university/student_detail_view.html', **{'student': s})


@view.route("/students", methods=["GET"])
def students():
    st_ = Student.query.all()
    return render_template('university/students.html', **{'students': st_})


@view.route("/universities/create", methods=["GET", "POST"])
@login_required
def create_uni():
    if request.method == "GET":
        return render_template("university/create_university.html")
    elif request.method == "POST":
        dt = datetime.datetime.fromisoformat(request.form.get("created_at"))
        university = University(created_at=dt, full_name=request.form.get("full_name"), short_name=request.form.get("short_name"))
        db.session.add(university)
        db.session.commit()
        db.session.refresh(university)

        return render_template("university/create_university.html")


@view.route("/students/create", methods=["GET", "POST"])
@login_required
def create_stu():
    universities_ = University.query.all()
    if request.method == "GET":
        return render_template("university/create_student.html", **{"universities": universities_})
    elif request.method == "POST":
        date_of_birth = datetime.datetime.fromisoformat(request.form.get("date_of_birth"))
        stu = Student(date_of_birth=date_of_birth, full_name=request.form.get("full_name"),
                      university_id=request.form.get("university_id"),
                      year_of_admission=request.form.get("year_of_admission"))
        db.session.add(stu)
        db.session.commit()
        db.session.refresh(stu)
        return render_template("university/create_student.html", **{"universities": universities_})


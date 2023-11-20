from flask import redirect, url_for, flash, Blueprint
from flask import render_template, request
from flask_login import login_user, current_user
from flask_login import logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from ..database.simple_models import UserSite, db


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already registered.", "info")
        return redirect(url_for("view.index"))
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = UserSite.query.filter_by(email=email).first()
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for('view.index'))
    return render_template("university/login.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        flash("You are already registered.", "info")
        return redirect(url_for("view.index"))
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = UserSite.query.filter_by(email=email).first()
        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        new_user = UserSite(email=email, name=name, password=generate_password_hash(password, method='scrypt'))

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template("university/signup.html")


@auth.route("/signout", methods=["GET"])
def signout():
    logout_user()
    return redirect(url_for('auth.login'))
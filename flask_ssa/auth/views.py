from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_user, logout_user
from flask_ssa.extensions import login_manager
from flask_ssa.auth.forms import LoginForm
from flask_ssa.auth.models import User

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user)

        #flash("Logged in successfully.", "success")
        return redirect(request.args.get("next") or url_for("main.home"))

    return render_template("login.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")

    return redirect(url_for("main.home"))


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)
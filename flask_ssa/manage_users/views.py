from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required
from flask_ssa.manage_users.forms import EditUser, AddUser
from flask_ssa.extensions import db
from flask_ssa.auth.models import User

manage_users = Blueprint('manage_users', __name__, url_prefix='/users', template_folder='templates')


@manage_users.route("/list_users")
@login_required
def list_users():
    users = User.query.order_by(User.surname).all()
    return render_template('list_users.html', users=users)


@manage_users.route("/edit_user/<username>", methods=["GET", "POST"])
@login_required
def edit_user(username):
    user = User.query.filter_by(username=username).one()
    form = EditUser(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for(".list_users"))

    return render_template('edit_user.html',form=form)


@manage_users.route("/add_user", methods=["GET", "POST"])
@login_required
def add_user():
    user = User()
    form = AddUser(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for(".list_users"))

    return render_template('edit_user.html',form=form)


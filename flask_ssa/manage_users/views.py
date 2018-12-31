from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_required, current_user
from flask_ssa.manage_users.forms import EditUser, AddUser
from flask_ssa.extensions import db
from flask_ssa.manage_users.models import User

manage_users = Blueprint('manage_users', __name__, url_prefix='/users', template_folder='templates')


def get_manager_list():
    users = User.query.filter(User.role.in_(['Manager','Regional Manager'])).all()
    result = []
    for user in users:
        result.append([user.emp_no, user.firstname + ' ' + user.surname ])
    return result


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
    form.manager_emp_no.choices = [('', '')]
    form.manager_emp_no.choices += get_manager_list()
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for(".list_users"))

    return render_template('edit_user.html',form=form, title='User details', user=user)


@manage_users.route("/add_user", methods=["GET", "POST"])
@login_required
def add_user():
    user = User()
    form = AddUser(obj=user)
    form.manager_emp_no.choices = [('', '')]
    form.manager_emp_no.choices += get_manager_list()
    if form.validate_on_submit():
        form.populate_obj(user)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for(".list_users"))

    return render_template('edit_user.html',form=form, title='New User')


@manage_users.route("/delete_user/<username>")
@login_required
def delete_user(username):
    if current_user.role == 'HQ':
        user = User.query.filter_by(username=username).one()
        db.session.delete(user)
        db.session.commit()
        flash("User has been deleted", "success")
    else:
        flash("You do not have permissions to delete the user", "warning")
    return redirect(url_for(".list_users"))

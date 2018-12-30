from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms import validators
from flask_ssa.manage_users.models import User


role_choices = [('', ''), ('Interviewer', 'Interviewer'), ('Manager', 'Manager'), ('Regional Manager', 'Regional Manager'),('HQ', 'HQ')]


class EditUser(FlaskForm):
    # username = StringField(u'Username', validators=[validators.required()])
    emp_no = StringField(u'Employee number', validators=[validators.required()])
    firstname = StringField(u'First name', validators=[validators.required()])
    surname = StringField(u'Surname', validators=[validators.optional()])
    role = SelectField(u'Role', choices=role_choices, validators=[validators.required()])
    manager_emp_no = SelectField(u'Manager employee number', choices=[], validators=[validators.required()])
    save = SubmitField('Save', id="save_button")

    def validate(self):
        check_validate = super(EditUser, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        return True


class AddUser(FlaskForm):
    username = StringField(u'Username', validators=[validators.required()])
    emp_no = StringField(u'Employee number', validators=[validators.required()])
    password = PasswordField(u'Password', validators=[validators.required()])
    firstname = StringField(u'First name', validators=[validators.required()])
    surname = StringField(u'Surname', validators=[validators.optional()])
    role = SelectField(u'Role', choices=role_choices, validators=[validators.required()])
    manager_emp_no = SelectField(u'Manager employee number', choices=[], validators=[validators.required()])
    save = SubmitField('Save', id="save_button")

    def validate(self):
        check_validate = super(AddUser, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        # check if user exists
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('User already exists')
            return False

        return True

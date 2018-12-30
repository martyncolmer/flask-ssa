from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators


class EditUser(FlaskForm):
    username = StringField(u'Username', validators=[validators.required()])
    firstname = StringField(u'First name', validators=[validators.required()])
    surname = StringField(u'Surname', validators=[validators.optional()])

    save = SubmitField('Save', id="save_button")

    def validate(self):
        check_validate = super(EditUser, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        return True


class AddUser(FlaskForm):
    username = StringField(u'Username', validators=[validators.required()])
    password = PasswordField(u'Password', validators=[validators.required()])
    firstname = StringField(u'First name', validators=[validators.required()])
    surname = StringField(u'Surname', validators=[validators.optional()])

    save = SubmitField('Save', id="save_button")

    def validate(self):
        check_validate = super(AddUser, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        return True

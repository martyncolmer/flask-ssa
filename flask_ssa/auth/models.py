from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_ssa.extensions import db, ma


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(255))
    emp_no = db.Column(db.String(20))
    firstname = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    role = db.Column(db.String(50))
    manager_emp_no = db.Column(db.String(20))
    api_key = db.Column(db.String(255))

    def __init__(self, username=None, password=None):
        if username:
            self.username = username
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


user_schema = UserSchema(strict=True)
users_schema = UserSchema(strict=True, many=True)
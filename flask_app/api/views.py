from flask import Blueprint, jsonify
from flask_app.extensions import login_manager
from flask_app.auth.models import User, users_schema, user_schema
from flask_login import current_user
import base64

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/listusers', methods=["POST"])
def listusers():
    if current_user.is_authenticated:
        userlist = User.query.all()
        results = users_schema.dumps(userlist)
        return jsonify(results)
    else:
        return auth_error()


@api.route('/getuser/<username>', methods=["POST"])
def getuser(username):
    if current_user.is_authenticated:
        thisuser = User.query.filter_by(username=username).first()
        results = user_schema.dumps(thisuser)
        return jsonify(results)
    else:
        return auth_error()


@api.errorhandler(401)
def auth_error(error=None):
    message = {
            'status': 401,
            'message': 'Authentication error',
    }
    resp = jsonify(message)
    resp.status_code = 401

    return resp


@login_manager.request_loader
def load_user_from_request(request):

    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
            api_key = api_key.decode().split(":")[-1]
        except TypeError:
            pass
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # finally, return None if both methods did not login the user
    return None

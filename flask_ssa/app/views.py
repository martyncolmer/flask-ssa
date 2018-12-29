from flask import Blueprint, render_template
from flask_login import login_required

from flask_ssa.extensions import cache

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
@cache.cached(timeout=1000)
def home():
    return render_template('index.html')


@main.route("/restricted")
@login_required
def restricted():
    return render_template('restricted_page.html')

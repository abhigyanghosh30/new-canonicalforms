from flask import Blueprint
from webapp.auth.decorators import login_required

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/', methods=['GET'])
@login_required
def index():
    """
    Admin index page.
    """
    return "Welcome to the Admin Dashboard"
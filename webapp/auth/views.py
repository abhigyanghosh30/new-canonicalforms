from flask import Blueprint

from webapp.auth.login import login_handler, logout

bp = Blueprint('auth', __name__, url_prefix='/auth')

bp.add_url_rule('/login', methods=['GET', 'POST'], view_func=login_handler)
bp.add_url_rule("/logout", view_func=logout)

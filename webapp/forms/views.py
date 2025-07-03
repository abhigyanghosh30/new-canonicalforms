from flask import Blueprint, render_template

bp = Blueprint("forms", __name__, url_prefix="/")
@bp.route("/<form_id>", methods=["GET"])
def index():
    """
    Forms index page.
    """
    return render_template("forms/index.html")
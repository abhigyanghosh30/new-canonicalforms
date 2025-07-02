import flask
from flask import Blueprint, render_template
from webapp.auth.decorators import login_canonicalstaff, login_required
from webapp.admin.models import db, FAForm

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/", methods=["GET"])
@login_required
def index():
    """
    Admin index page.
    """
    forms = db.session.execute(db.select(FAForm).order_by(FAForm.title)).scalars()
    return render_template("admin/index.html", forms=forms)


@login_canonicalstaff
@bp.route("/fa-form/add", methods=["GET", "POST"])
def add_fa_form():
    if flask.request.method != "POST":
        return render_template("admin/fa-form/add.html")

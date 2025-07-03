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
    if flask.request.method == "GET":
        return render_template("admin/fa-form/add.html")
    elif flask.request.method == "POST":
        id = flask.request.form.get("id")
        title = flask.request.form.get("title")
        description = flask.request.form.get("description")
        require_login = flask.request.form.get("require_login") == "on"
        raw_content = flask.request.form.get("raw_content")
        require_js = flask.request.form.get("require_js") == "on"
        thanks_page = flask.request.form.get("thanks_page")

        form = FAForm(
            id=id,
            title=title,
            description=description,
            require_login=require_login,
            raw_content=raw_content,
            require_js=require_js,
            thanks_page=thanks_page,
        )
        db.session.add(form)
        db.session.commit()
        return flask.redirect(flask.url_for("admin.index"))
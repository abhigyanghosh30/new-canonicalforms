import flask
from flask import Blueprint, render_template
from webapp.auth.decorators import login_canonicalstaff, login_required
from webapp.admin.models import ThanksPage, db, FAForm

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
        form_link = flask.request.form.get("form_link")
        require_js = flask.request.form.get("require_js") == "on"
        thanks_page = flask.request.form.get("thanks_page")

        form = FAForm(
            id=id,
            title=title,
            description=description,
            require_login=require_login,
            form_link=form_link,
            require_js=require_js,
            thanks_page=thanks_page,
        )
        db.session.add(form)
        db.session.commit()
        return flask.redirect(flask.url_for("admin.index"))

@login_canonicalstaff
@bp.route("/fa-form/<formid>/edit", methods=["GET", "POST"])
def edit_fa_form(formid):
    form = db.session.execute(db.select(FAForm).filter_by(id=formid)).scalar_one_or_none()
    if not form:
        flask.abort(404)

    if flask.request.method == "GET":
        return render_template("admin/fa-form/edit.html", form=form)
    elif flask.request.method == "POST":
        form.title = flask.request.form.get("title")
        form.description = flask.request.form.get("description")
        form.require_login = flask.request.form.get("require_login") == "on"
        form.form_link = flask.request.form.get("form_link")
        form.require_js = flask.request.form.get("require_js") == "on"
        form.thanks_page = flask.request.form.get("thanks_page")
        form.launchpad_teams = flask.request.form.get("launchpad_team", "").strip()
        db.session.commit()
        return flask.redirect(flask.url_for("admin.index"))
    

@login_canonicalstaff
@bp.route("/fa-form/<formid>/duplicate", methods=["GET"])
def duplicate_fa_form(formid):
    form = db.session.execute(db.select(FAForm).filter_by(id=formid)).scalar_one_or_none()
    if not form:
        flask.abort(404)

    new_form = FAForm(
        id=form.id + "-copy",
        title=form.title + " (Copy)",
        description=form.description,
        require_login=form.require_login,
        form_link=form.form_link,
        require_js=form.require_js,
        thanks_page=form.thanks_page,
        launchpad_teams=form.launchpad_teams
    )
    return flask.render_template("admin/fa-form/edit.html", form=new_form)


@login_canonicalstaff
@bp.route("/fa-form/<formid>/delete", methods=["GET"])
def delete_fa_form(formid):
    form = db.session.execute(db.select(FAForm).filter_by(id=formid)).scalar_one_or_none()
    if not form:
        flask.abort(404)

    db.session.delete(form)
    db.session.commit()
    return flask.redirect(flask.url_for("admin.index"))


@login_canonicalstaff
@bp.route("/thanks-page/add", methods=["GET", "POST"])
def add_thanks_page():
    if flask.request.method == "GET":
        return render_template("admin/thanks-page/add.html")
    elif flask.request.method == "POST":
        name = flask.request.form.get("name")
        title = flask.request.form.get("title")
        content = flask.request.form.get("content")

        thanks_page = ThanksPage(name=name, title=title, content=content)
        db.session.add(thanks_page)
        db.session.commit()
        return flask.redirect(flask.url_for("admin.index"))
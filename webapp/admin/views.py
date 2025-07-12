import os
import flask
from flask import Blueprint, render_template, url_for
from webapp.auth.decorators import login_canonicalstaff, login_required
from webapp.admin.models import ThanksPage, db, FAForm

bp = Blueprint("admin", __name__, url_prefix="/admin")


@login_canonicalstaff
@bp.route("/", methods=["GET"])
def index():
    """
    Admin index page.
    """
    forms = db.session.execute(db.select(FAForm).order_by(FAForm.title)).scalars()
    pages = db.session.execute(db.select(ThanksPage).order_by(ThanksPage.title)).scalars()
    return render_template("admin/index.html", forms=forms, pages=pages)


@login_canonicalstaff
@bp.route("/fa-form", methods=["GET"])
def view_forms():
    """
    View all forms.
    """
    forms = db.session.execute(db.select(FAForm).order_by(FAForm.title)).scalars()
    return render_template("admin/fa_forms/index.html", forms=forms)


@login_canonicalstaff
@bp.route("/fa-form/add", methods=["GET", "POST"])
def add_fa_form():
    if flask.request.method == "GET":
        return render_template("admin/fa_forms/add.html")
    elif flask.request.method == "POST":
        id = flask.request.form.get("id")
        title = flask.request.form.get("title")
        description = flask.request.form.get("description")
        require_login = flask.request.form.get("require_login") == "on"
        form_link = flask.request.form.get("form_link")

        form = FAForm(
            id=id,
            title=title,
            description=description,
            require_login=require_login,
            form_link=form_link,
        )
        db.session.add(form)
        db.session.commit()
        return flask.redirect(flask.url_for("admin.index"))


@login_canonicalstaff
@bp.route("/fa-form/<formid>/edit", methods=["GET", "POST"])
def edit_fa_form(formid):
    form = db.session.execute(
        db.select(FAForm).filter_by(id=formid)
    ).scalar_one_or_none()
    if not form:
        flask.abort(404)

    print(form.require_login)

    if flask.request.method == "GET":
        return render_template("admin/fa_forms/add.html", form=form)
    elif flask.request.method == "POST":
        form.id = flask.request.form.get("id")
        form.title = flask.request.form.get("title")
        form.description = flask.request.form.get("description")
        form.form_link = flask.request.form.get("form_link")
        form.require_login = flask.request.form.get("require_login") == "on"
        form.launchpad_teams = flask.request.form.get("launchpad_team", "").strip()
        db.session.commit()
        return flask.redirect(flask.url_for("admin.index"))


@login_canonicalstaff
@bp.route("/fa-form/<formid>/duplicate", methods=["GET"])
def duplicate_fa_form(formid):
    form = db.session.execute(
        db.select(FAForm).filter_by(id=formid)
    ).scalar_one_or_none()
    if not form:
        flask.abort(404)

    new_form = FAForm(
        id=form.id + "-copy",
        title=form.title + " (Copy)",
        description=form.description,
        form_link=form.form_link,
        require_login=form.require_login,
        launchpad_teams=form.launchpad_teams,
    )
    db.session.add(new_form)
    db.session.commit()
    return flask.render_template("admin/fa_forms/add.html", form=new_form)


@login_canonicalstaff
@bp.route("/fa-form/<formid>/delete", methods=["GET"])
def delete_fa_form(formid):
    form = db.session.execute(
        db.select(FAForm).filter_by(id=formid)
    ).scalar_one_or_none()
    if not form:
        flask.abort(404)

    db.session.delete(form)
    db.session.commit()
    return flask.redirect(flask.url_for("admin.index"))


@login_canonicalstaff
@bp.route("/thanks-page", methods=["GET"])
def view_thanks_pages():
    """
    View all thanks pages.
    """
    thanks_pages = db.session.execute(db.select(ThanksPage).order_by(ThanksPage.title)).scalars()
    return render_template("admin/thanks_pages/index.html", pages=thanks_pages)

@login_canonicalstaff
@bp.route("/thanks-page/add", methods=["GET", "POST"])
def add_thanks_page():
    if flask.request.method == "GET":
        return render_template("admin/thanks_pages/add.html")
    elif flask.request.method == "POST":
        name = flask.request.form.get("name")
        title = flask.request.form.get("title")
        content = flask.request.form.get("content")

        thanks_page = ThanksPage(name=name, title=title, content=content)
        db.session.add(thanks_page)
        db.session.commit()
        return flask.redirect(flask.url_for("admin.index"))


@login_canonicalstaff
@bp.route("/thanks-page/<thanks_page_name>/edit", methods=["GET", "POST"])
def edit_thanks_page(thanks_page_name):
    thanks_page = db.session.execute(
        db.select(ThanksPage).filter_by(name=thanks_page_name)
    ).scalar_one_or_none()
    if not thanks_page:
        flask.abort(404)

    if flask.request.method == "GET":
        return render_template("admin/thanks_pages/add.html", form=thanks_page)
    elif flask.request.method == "POST":
        thanks_page.title = flask.request.form.get("title")
        thanks_page.content = flask.request.form.get("content")
        db.session.commit()
        return flask.redirect(flask.url_for("admin.index"))

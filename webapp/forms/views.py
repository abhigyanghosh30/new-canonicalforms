import flask
from webapp.admin.models import FAForm
from flask import render_template, abort

from webapp.auth.launchpad import check_user_in_team
from webapp.auth.login import user_info


def render_form(formid):
    """
    Render a form based on its ID.
    """

    form = FAForm.query.filter_by(id=formid).first()
    if not form:
        abort(404)

    if form.require_login and "openid" not in flask.session:
        return flask.redirect(flask.url_for("auth.login", next=flask.request.path))

    user = user_info(flask.session)
    if not user and form.require_login:
        return flask.redirect(flask.url_for("auth.login", next=flask.request.path))

    if form.launchpad_teams != "" and user:
        for team in form.launchpad_teams.split(","):
            if not check_user_in_team(user.email, team.strip()):
                return flask.redirect(
                    flask.url_for("auth.login", next=flask.request.path)
                )

    return render_template("forms/base_canonical_form.html", form=form)

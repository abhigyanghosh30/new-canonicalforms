# Core packages
import functools

# Third party packages
import flask
from webapp.auth.launchpad import check_user_in_team
from webapp.auth.login import user_info


def login_required(func):
    """
    Decorator that checks if a user is logged in, and redirects
    to login page if not.
    """

    @functools.wraps(func)
    def is_user_logged_in(*args, **kwargs):
        if not user_info(flask.session):
            return flask.redirect("/auth/login?next=" + flask.request.path)

        return func(*args, **kwargs)

    return is_user_logged_in


def login_canonicalstaff(func):
    """
    Decorator that checks if a user is canonical staff in, and redirects
    to login page if not.
    """

    @functools.wraps(func)
    def is_user_logged_in(*args, **kwargs):
        user = user_info(flask.session)
        if not user or not user.email.endswith("@canonical.com"):
            return flask.redirect("/auth/login?next=" + flask.request.path)
        return func(*args, **kwargs)

    return is_user_logged_in


def login_with_teams_required(team):
    """
    Decorator that checks if a user is logged in and a member of a specific team.
    Redirects to login page if not logged in or not a member of the team.
    """
    def is_user_in_team(func):
        def wrapper(*args, **kwargs):
            user = user_info(flask.session)
            if not user:
                return flask.redirect("/auth/login?next=" + flask.request.path)

            email = user.get("email")

            if check_user_in_team(email, team):
                return func(*args, **kwargs)

            return flask.render_template("errors/401_unauthorized.html")
        return wrapper

    return is_user_in_team
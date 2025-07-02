import os
import flask
import flask_openid


login_url = os.getenv("CANONICAL_LOGIN_URL", "https://login.ubuntu.com")
open_id = flask_openid.OpenID(
    store_factory=lambda: None,
    safe_roots=[],
)


def user_info(user_session):
    """
    Checks if the user is authenticated from the session
    Returns True if the user is authenticated
    """

    if "openid" in user_session:
        return {
            "fullname": user_session["openid"]["fullname"],
            "email": user_session["openid"]["email"],
        }
    else:
        return None


def empty_session(user_session):
    """
    Remove items from session
    """

    user_session.pop("openid", None)


@open_id.loginhandler
def login_handler():
    if user_info(flask.session):
        return flask.redirect(open_id.get_next_url())
    return open_id.try_login(
        login_url,
        ask_for=["email", "nickname", "image"],
        ask_for_optional=["fullname"],
    )


@open_id.after_login
def after_login(resp):
    if not resp.nickname:
        return flask.redirect(login_url)

    flask.session["openid"] = {
        "identity_url": resp.identity_url,
        "nickname": resp.nickname,
        "fullname": resp.fullname,
        "image": resp.image,
        "email": resp.email,
    }
    return flask.redirect(open_id.get_next_url())


def logout():
    return_to = flask.request.args.get("return_to") or flask.request.path

    # Protect against redirect loop if return_to is logout
    if return_to == "/logout":
        return_to = "/"

    empty_session(flask.session)

    return flask.redirect(return_to)

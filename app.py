import os
import flask

from slugify import slugify

from flask import redirect

from webapp.auth import views as auth_views
from webapp.admin import views as admin_views
from webapp.admin.models import db
from webapp.context import build_navigation, split_list, versioned_static
from webapp.forms.views import render_form
from webapp.thanks.views import render_thanks_page

app = flask.Flask(__name__)
app.config.from_prefixed_env()

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("POSTGRESQL_DB_CONNECT_STRING")
db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(admin_views.bp)
app.register_blueprint(auth_views.bp)

app.add_url_rule("/<formid>", view_func=render_form, methods=["GET"])
app.add_url_rule("/thanks/<thanks_page_name>", view_func=render_thanks_page, methods=["GET"])

@app.route("/")
def index():
    return redirect("https://canonical.com")


@app.errorhandler(401)
def unauthorized(e):
    return flask.render_template("/errors/401_unauthorized.html"), 401


@app.errorhandler(404)
def not_found(e):
    return flask.render_template("errors/404_notfound.html"), 404


@app.errorhandler(500)
def internal_error(e):
    return flask.render_template("errors/500_error.html"), 500


@app.context_processor
def context():
    return {
        "build_navigation": build_navigation,
        "split_list": split_list,
        "versioned_static": versioned_static,
    }


@app.template_filter()
def slug(text):
    return slugify(text)


if __name__ == "__main__":
    app.run()

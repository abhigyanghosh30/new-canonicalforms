from flask import render_template, abort
from webapp.admin.models import ThanksPage


def render_thanks_page(thanks_page_name):
    """
    Render a thanks page based on its name.
    """
    thanks_page = ThanksPage.query.filter_by(name=thanks_page_name).first()
    if not thanks_page:
        abort(404)

    return render_template("thanks_page.html", title=thanks_page.title, content=thanks_page.content)
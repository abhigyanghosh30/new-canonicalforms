from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class FAForm(db.Model):
    id = db.Column(db.String(30), primary_key=True)
    title = db.Column(db.String(1024), unique=True)
    description = db.Column(db.String(1024))
    require_login = db.Column(db.Boolean)
    raw_content = db.Column(db.Text)
    require_js = db.Column(db.Boolean)
    thanks_page = db.Column(db.String(1024), db.ForeignKey("thanks_page.name"))


class ThanksPage(db.Model):
    name = db.Column(db.String(1024), primary_key=True)
    title = db.Column(db.String(1024), unique=True)
    content = db.Column(db.Text)

from flask_ckeditor import CKEditor

ckeditor = CKEditor()


def init_app(app):
    ckeditor.init_app(app)
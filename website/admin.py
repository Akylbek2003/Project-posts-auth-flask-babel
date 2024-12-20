from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from website.models import User, Note
from website.views import UserView, NoteAdmin

def initialize_admin(app, db):
    admin = Admin(app, name='Админ', template_mode='bootstrap4')
    # admin.add_view(UserView(User, db.session, name='Users'))
    # admin.add_view(ModelView(Post, db.session, name='Post'))
    # admin.add_view(ModelView(Tag, db.session))
    # admin.add_view(ModelView(Comment, db.session))
    admin.add_view(NoteAdmin(Note, db.session, name='Посты'))
    return app



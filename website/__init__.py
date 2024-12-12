from flask import Flask, g, request, session
from flask_babel import Babel, _, lazy_gettext as _l, gettext
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'qwertyuiop[]'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = './translations'
    
    db.init_app(app)

    def get_locale():
        # Устанавливаем значение lang по умолчанию
        lang = None

        # Проверяем язык в запросе
        if 'lang' in request.args:
            lang = request.args.get('lang')
            if lang in ['en', 'ru']:
                session['lang'] = lang  # Сохраняем язык в сессии
                return lang

        # Если язык уже сохранён в сессии
        if 'lang' in session:
            return session.get('lang')

        # Используем язык браузера
        return request.accept_languages.best_match(['en', 'ru'])

    babel = Babel(app, locale_selector=get_locale)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created Database!")

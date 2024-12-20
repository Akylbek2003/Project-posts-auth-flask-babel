from flask import Blueprint, render_template, request, flash,  redirect, url_for, session, g, current_app
from flask_login import login_required, current_user
from .models import Note 
from . import db
import json
from website.service import get_locale
from flask_admin.contrib.sqla import ModelView
import uuid, os
from flask_babel import Babel, _, lazy_gettext as _l, gettext
from flask_admin import form
from markupsafe import Markup 
from wtforms import validators
from flask_admin.form import ImageUploadField

file_path = os.path.abspath(os.path.dirname(__name__))


# Функция, которая будет генерировать имя файла из модели и загруженного файлового объекта.
def name_gen_image(model, file_data):
    hash_name = f'{model}/{model.username}'
    return hash_name

class NoteAdmin(ModelView):
    column_list = ('id', 'username','title', 'content', 'date', 'image_post', 'user_id')  # Поля для отображения
    form_columns = ('title', 'content', 'image_post', 'user_id')  # Поля для редактирования
    column_searchable_list = ['title', 'content']
    column_filters = ['date']
    column_labels = {
        'id' : 'ID',
        'username' : 'Имя пользователя',
        'title': 'Титул',
        'content': 'Контент',
        'date': 'Дата',
        'image_post': 'Картинка поста',
    }
    
    form_overrides = {
        'image_post': ImageUploadField
    }
    form_args = {
        'image_post': {
            'base_path': 'website/static/uploads',
            'allowed_extensions': ['jpg']
        }
    }
    

    # Отображение миниатюры в списке постов
    def _list_thumbnail(view, context, model, name):
        if not model.image_post:
            return ''

        url = url_for('static', filename=os.path.join('uploads/', model.image_post))
        if model.image_post.split('.')[-1] in ['jpg', 'jpeg', 'png', 'svg', 'gif']:
            return Markup(f'<img src={url} width="100">')

    column_formatters = {
        'image_post': _list_thumbnail
    }

    form_extra_fields = {
        # ImageUploadField Выполняет проверку изображений, создание эскизов, обновление и удаление изображений.
        "image_post": form.ImageUploadField('',
                                            # Абсолютный путь к каталогу, в котором будут храниться файлы
                                            base_path=
                                            os.path.join(file_path, 'website/static/uploads/'),
                                            # Относительный путь из каталога. Будет добавляться к имени загружаемого файла.
                                            url_relative_path='uploads/',
                                            namegen=name_gen_image,
                                            # Список разрешенных расширений. Если не указано, то будут разрешены форматы gif, jpg, jpeg, png и tiff.
                                            allowed_extensions=['jpg'],
                                            max_size=(1200, 780, True),
                                            thumbnail_size=(100, 100, True),

                                            )}

    form_overrides = {
        'image_post': ImageUploadField
    }


class UserView(ModelView):
    column_display_pk = True
    column_labels = {
        'id' : 'ID',
        'username': 'Имя пользователья',
        'last_seen': 'Последний вход',
        'image_user': 'Аватар',
        'posts': 'Посты',
        'email': 'Емайл',
        'password': 'Пароль',
        'role': 'Роль',
        'file': 'Выберите изображение'
    }

    column_list = ['id', 'role', 'username', 'email', 'password', 'last_seen', 'image_user']
    
    column_default_sort = ('username', True)
    column_sotrable_list = ('id', 'role', 'username', 'email')

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image = request.files.get('image_post')

        # Проверка на наличие данных
        if not title or not content:
            flash(_('Title and content are required!'), category='error')
        else:
            image_filename = None

            # Если пользователь загрузил изображение
            if image:
                # Генерация уникального имени файла
                image_filename = f"{uuid.uuid4().hex}_{image.filename}"
                upload_path = os.path.join(current_app.root_path, 'static/uploads', image_filename)
                image.save(upload_path)

            # Создание новой заметки
            new_note = Note(
                title=title,
                content=content,
                image_post=image_filename,
                user_id=current_user.id
            )
            db.session.add(new_note)
            db.session.commit()
            flash(_('Note added!'), category='success')

    return render_template("home.html", user=current_user)
    
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})


@views.context_processor
def inject_locale():
    return {'get_locale': get_locale}

@views.route('/setlang')
def setlang():
    lang = request.args.get('lang', 'en')
    session['lang'] = lang
    return redirect(request.referrer or '/')

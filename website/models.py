from flask import url_for
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):  # Ранее была Post
    __tablename__ = 'note'  # Имя таблицы, можно оставить "post" для совместимости
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=True)
    title = db.Column(db.String(120), nullable=True)  # Заголовок поста
    content = db.Column(db.Text, nullable=True)  # Текст поста
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime, default=func.now())  # Дата создания
    image_post = db.Column(db.String(255), nullable=True, default='default.jpg')  # Картинка поста
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Автор поста
    tags = db.relationship('Tag', backref='tag_post', lazy=True, cascade="all, delete-orphan")  # Теги
    
    def __repr__(self):
        return f"Post {self.title}"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    post_id = db.Column(db.Integer, db.ForeignKey('note.id'))  # Изменили на note.id
    def __repr__(self):
        return self.name 


from flask import  request, session
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

# # Создаём функцию для выбора локали
# def get_locale():
#     # Проверяем язык в запросе
#     if 'lang' in request.args:
#         lang = request.args.get('lang')
#     if lang in ['en', 'ru']:
#         session['lang'] = lang  # Сохраняем язык в сессии
#         return lang
#     # Если язык уже сохранён в сессии
#     if 'lang' in session:
#         return session.get('lang')
#     # Используем язык браузера
#     return request.accept_languages.best_match(['en', 'ru'])
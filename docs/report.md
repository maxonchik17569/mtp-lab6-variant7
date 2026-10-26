# Отчёт по лабораторной работе №6

Ким Максим Сергеевич, группа 221341, вариант 7.

Работа выполнена на Python 3.13.14. Пакет `lab6` содержит четыре
независимых приложения: два на FastAPI и два на Flask. Тесты не
открывают сетевые порты: FastAPI проверяется через `TestClient`,
Flask — через `test_client()`.

## Средняя сложность

### №7. FastAPI-эндпоинт возвращает JSON

Файл `lab6/json_api.py`. Приложение `FastAPI` с маршрутом
`GET /api/status` возвращает JSON:

```json
{
  "service": "lab6-json-api",
  "status": "ok",
  "variant": 7
}
```

Ответ описан Pydantic-моделью `StatusResponse`, поэтому FastAPI
проверяет структуру и отдаёт `application/json`. Тесты
`tests/test_json_api.py` проверяют код 200, MIME-тип, точный набор
полей и значение варианта.

### №9. Шаблон Jinja2 с данными

Файлы `lab6/template_app.py` и `lab6/templates/books.html`. Flask-
приложение с маршрутом `GET /` передаёт в шаблон список из четырёх
книг. В шаблоне используются:

- цикл `{% for book in books %}`;
- условие `{% if book.available %}` для статуса «доступна»/«выдана»;
- условие `{% if book.year < 1970 %}` для метки «Классика»;
- `{% if loop.last %}` для отметки последней книги.

Фабрика `create_app(books=None)` позволяет подставить свой список;
по умолчанию используется `BOOKS`. Тесты `tests/test_template_app.py`
проверяют рендеринг всех книг, обе ветки условия доступности, метку
классики, отметку последней книги и работу с пользовательским списком.

### №3. Статическая страница и CSS

Файлы `lab6/static_app.py`, `lab6/templates/about.html` и
`lab6/static/style.css`. Flask отдаёт страницу `GET /` из шаблона
`about.html`, в котором подключён `static/style.css` через
`url_for('static', filename='style.css')`. CSS задаёт цветовые
переменные, фон, отступы, карточку, список фактов, кнопку и
адаптивное поведение на узких экранах. Тесты
`tests/test_static_app.py` проверяют код 200, содержимое страницы,
подключение стилей, выдачу CSS с MIME-типом `text/css` и наличие
цветов/отступов в файле.

## Повышенная сложность

### №7. Деплой на Heroku

Подготовлены `Procfile`, `app.json` и `docs/heroku.md`.

`Procfile`:

```text
web: uvicorn lab6.notes_api:app --host 0.0.0.0 --port $PORT
```

`app.json` содержит buildpack `heroku/python` и
`PYTHONUNBUFFERED=1`; web-процесс объявлен в `Procfile`.
В `docs/heroku.md` описаны команды
`heroku login`, `heroku create APP_NAME`, `git push heroku main`,
проверка `/docs` и `/notes`, а также просмотр логов.

Проверена конфигурация, а не живой деплой:

- `app.json` успешно разбирается как JSON;
- строка запуска в `Procfile` совпадает с требуемой;
- приложение `lab6.notes_api:app` импортируется и проходит тесты.

Реальный деплой не выполнялся: аккаунта Heroku нет. Поэтому
утверждение «приложение работает на Heroku» в отчёте не делается.

### №5. REST API заметок

Файл `lab6/notes_api.py`. Используются Pydantic-модели:

- `NoteCreate` — обязательные `title` и `text`; заголовок
  обрезается по краям и не может быть пустым;
- `Note` — те же поля плюс `id`.

Хранилище `NoteStore` держит заметки в словаре и выдаёт
последовательные идентификаторы. Фабрика `create_app(store=None)`
создаёт приложение с отдельным хранилищем; это исключает общее
изменяемое состояние между тестами. Для uvicorn в модуле есть
глобальный `app = create_app()`.

| Метод | Путь | Успех | Ошибка |
| --- | --- | --- | --- |
| GET | `/notes` | 200, список | — |
| GET | `/notes/{id}` | 200, заметка | 404 |
| POST | `/notes` | 201, созданная заметка | 422 |
| PUT | `/notes/{id}` | 200, заменённая заметка | 404, 422 |
| DELETE | `/notes/{id}` | 204, пустое тело | 404 |

Тесты `tests/test_notes_api.py` проверяют пустой список, создание,
чтение, замену, удаление, коды 201/204/404/422, нормализацию
заголовка и изоляцию двух независимых хранилищ.

## Проверки

### Тесты

Команда:

```bash
uv run --python 3.13 --with flask --with fastapi --with httpx \
  --with flake8 python -m unittest discover -s tests -v
```

Фрагмент вывода:

```text
Ran 25 tests in 0.160s

OK
```

Тесты покрывают все четыре приложения и CRUD заметок. В stderr
появляется предупреждение `StarletteDeprecationWarning` про `httpx`
внутри `fastapi.testclient`; это предупреждение сторонней
библиотеки, на результат оно не влияет.

### Стиль кода

```bash
uv run --with flake8 flake8 lab6 tests
```

Команда завершилась с кодом 0 и не вывела замечаний.

### Демонстрация

```bash
uv run --python 3.13 --with flask --with fastapi --with httpx \
  python -m lab6
```

Вывод (сетевые порты не открываются):

```text
Лабораторная работа №6, вариант 7
Средняя сложность
json_api GET /api/status -> 200 {'service': 'lab6-json-api', 'status': 'ok', 'variant': 7}
template_app GET / -> 200, книг в шаблоне: 4
static_app GET / -> 200, CSS: 200
static_app GET /static/style.css -> 200 text/css; charset=utf-8
Повышенная сложность
notes_api POST /notes -> 201 {'title': 'Подготовить отчёт', 'text': 'Проверить CRUD', 'id': 1}
notes_api GET /notes -> 200 [{'title': 'Подготовить отчёт', 'text': 'Проверить CRUD', 'id': 1}]
notes_api PUT /notes/1 -> 200 {'title': 'Сдать отчёт', 'text': 'CRUD проверен', 'id': 1}
notes_api DELETE /notes/1 -> 204
notes_api GET /notes/1 -> 404
Heroku: Procfile и app.json подготовлены, живой деплой не выполнялся.
Серверы можно запустить командами из README.md.
```

### CI

`.github/workflows/python-checks.yml` использует Python 3.13,
устанавливает `requirements-dev.txt`, запускает `flake8 lab6 tests`,
`python -m compileall -q lab6 tests` и
`python -m unittest discover -s tests -v`.

## Ограничения

- Живой деплой на Heroku не выполнялся; проверена только
  конфигурация.
- Заметки хранятся в памяти процесса и исчезают при перезапуске.
- `git init`, коммиты и теги не создавались: история передаётся
  родительскому репозиторию.

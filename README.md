# Лабораторная работа №6

Ким Максим Сергеевич, группа 221341, вариант 7, лабораторная №6.

Учебный проект по веб-программированию на Python: Flask, FastAPI и
Jinja2. Все проверки выполняются через тестовые клиенты, сетевые порты
для тестов не открываются.

## Задания варианта

**Средняя сложность:**

- №7 — FastAPI-эндпоинт возвращает JSON (`lab6/json_api.py`)
- №9 — шаблон Jinja2 с данными (`lab6/template_app.py`,
  `lab6/templates/books.html`)
- №3 — статическая страница и CSS (`lab6/static_app.py`,
  `lab6/templates/about.html`, `lab6/static/style.css`)

**Повышенная сложность:**

- №7 — подготовка деплоя на Heroku (`Procfile`, `app.json`,
  `docs/heroku.md`)
- №5 — REST API заметок (`lab6/notes_api.py`)

## Клонирование

```bash
git clone https://github.com/maxonchik17569/mtp-lab6-variant7.git
cd mtp-lab6-variant7
```

## Запуск

Демонстрация без открытия портов (используются `TestClient` и
`test_client()`):

```bash
uv run --with flask --with fastapi --with httpx python -m lab6
```

Запуск HTTP-серверов (открывает порт; `Ctrl+C` — остановить):

```bash
uv run --with fastapi --with uvicorn \
  uvicorn lab6.json_api:app --reload
uv run --with flask flask --app lab6.template_app run --debug
uv run --with flask flask --app lab6.static_app run --debug
uv run --with fastapi --with uvicorn \
  uvicorn lab6.notes_api:app --reload
```

После запуска `notes_api` интерактивная документация доступна по
адресу `http://127.0.0.1:8000/docs`.

## Проверки

```bash
uv run --with flask --with fastapi --with httpx --with flake8 \
  python -m unittest discover -s tests -v
uv run --with flake8 flake8 lab6 tests
```

Ожидаемый результат: 25 тестов, `OK`; `flake8` завершается с кодом 0
без замечаний.

## Heroku

Файлы `Procfile` и `app.json` содержат конфигурацию для Heroku, а
пошаговая инструкция с плейсхолдером `APP_NAME` находится в
[docs/heroku.md](docs/heroku.md). Живой деплой в рамках лабораторной
не выполнялся: проверена конфигурация, а не реальный запуск на Heroku.

## Структура

```text
lab6/
  __main__.py       демонстрация без сети
  json_api.py       FastAPI, GET /api/status
  template_app.py   Flask + Jinja2, GET /
  static_app.py     Flask, GET / и /static/style.css
  notes_api.py      FastAPI, CRUD /notes
  templates/        books.html, about.html
  static/           style.css
tests/              unittest-тесты всех заданий
docs/               report.md, heroku.md
```

# Деплой на Heroku

Инструкция описывает подготовку и проверку конфигурации. Реальный
деплой в рамках лабораторной не выполнялся: нет аккаунта Heroku.
Имя приложения и адрес заменены плейсхолдером `APP_NAME`.

## Что уже подготовлено

- `Procfile` — команда запуска:
  `web: uvicorn lab6.notes_api:app --host 0.0.0.0 --port $PORT`.
- `app.json` — описание приложения, buildpack `heroku/python` и
  переменная `PYTHONUNBUFFERED=1`; web-процесс объявлен в `Procfile`.
- `requirements.txt` — зависимости, которые установит Heroku.
- Приложение `lab6.notes_api:app` автоматически отдаёт `/docs`.

## Пошаговый деплой

1. Установите Heroku CLI и войдите в аккаунт:

   ```bash
   heroku login
   ```

2. Создайте приложение (вместо `APP_NAME` укажите своё имя):

   ```bash
   heroku create APP_NAME
   ```

3. Проверьте, что buildpack — Python:

   ```bash
   heroku buildpacks:set heroku/python
   ```

4. Убедитесь, что remote `heroku` появился:

   ```bash
   git remote -v
   ```

5. Отправьте ветку `main` на Heroku:

   ```bash
   git push heroku main
   ```

6. Убедитесь, что web-процесс запущен:

   ```bash
   heroku ps:scale web=1
   heroku ps
   ```

7. Посмотрите логи, если приложение не отвечает:

   ```bash
   heroku logs --tail
   ```

8. Откройте приложение и проверьте документацию и API:

   ```bash
   heroku open
   curl https://APP_NAME.herokuapp.com/docs
   curl https://APP_NAME.herokuapp.com/notes
   ```

   Ожидаемые ответы: `/docs` отдаёт HTML-страницу Swagger UI,
   `/notes` — JSON-массив (сначала пустой: `[]`).

## Проверка конфигурации без деплоя

Локально можно проверить JSON-файл и команду из `Procfile`:

```bash
uv run python -m json.tool app.json > /dev/null
grep '^web: uvicorn lab6.notes_api:app' Procfile
```

## Ограничения

- Живой деплой, масштабирование dyno и проверка внешнего URL не
  выполнялись.
- Значения переменных окружения и токены в репозиторий не добавляются.
- Приложение хранит заметки в памяти: после перезапуска dyno данные
  теряются. Для лабораторной этого достаточно.

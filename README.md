# Foodgram

## Установка и запуск проекта

1. Клонируйте репозиторий:
```bash
git clone https://github.com/grannnsacker/foodgram-st.git
```

2. Соберите статические файлы:
```bash
docker-compose exec backend python manage.py collectstatic
```

3. Запустите проект:
```bash
docker-compose up --build
```

4. Примените миграции:
```bash
docker-compose exec backend python manage.py migrate
```

5. Загрузите ингредиенты в базу данных:
```bash
docker-compose exec backend python manage.py load_ingredients /app/data/ingredients.json
```

## Создание суперпользователя

Для создания суперпользователя выполните команду:
```bash
docker-compose exec backend python manage.py createsuperuser
```

## Доступ к проекту

После запуска проекта:
- Проект будет доступен по адресу: http://localhost/
- Админ-панель: http://localhost/admin/


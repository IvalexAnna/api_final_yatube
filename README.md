## api_yatube
Данный проект - социальная сеть, которая позволяет пользователям создавать посты, комментировать их и объединять посты в группы. Эта работа реализована с использованием Django и предоставляет RESTful API для взаимодействия с данными.
## В проекте api_yatube есть четыре приложения:
-yatube_api главное приложение
-posts с описанием моделей Yatube
-api с описанием логики API для моделей
-static с файлом redoc.yaml

## Содержание:
- [Описание проекта](#описание-проекта)
- [Как развернуть](#как-развернуть)
- [Информация об авторе](#информация-об-авторе)
- [Примеры запросов и ответов](#примеры-запросов-и-ответов)
## Описание проекта
Проект включает в себя следующие модели:
- **Group**: Модель для групп, в которые можно объединять посты. Каждая группа имеет заголовок, уникальный слаг и описание.
- **Post**: Модель для постов, которые могут содержать текст, дату публикации, автора, изображение и принадлежать к определенной группе.
- **Comment**: Модель для комментариев к постам. Каждый комментарий связан с автором и конкретным постом, а также содержит текст комментария и дату его создания.
- **Follow**: Модель описывает систему подписок между пользователями в приложении.
- **Group**: Модель описывает группу или в контексте приложения.
## Как развернуть
Инструкции по развертыванию проекта локально:
1. Клонируйте репозиторий:
```bash
   `git clone https://github.com/IvalexAnna/api_final_yatube`
```

2. Перейдите в директорию проекта:
```bash

    `cd ваш_репозиторий`

```

3. Cоздайте и активируйте виртуальное окружение:

```bash

    `python -m venv venv`

    `source venv/Scripts/activate`

```

4. Установите зависимости:
```bash

    `pip install -r requirements.txt`

```
  
5. Выполните миграции базы данных:
```bash

    `python manage.py migrate`

```

6. Создайте суперпользователя:
```bash

    `python manage.py createsuperuser`

```

7. Запустите сервер разработки:
```bash

    `python manage.py runserver`

 ```

8. Теперь вы можете открыть браузер и перейти по адресу http://127.0.0.1:8000/.

**Информация об авторе проекта, сделанного в рамках практической работы Яндекс Практикума:**
Имя автора: Иванова Анна
Контактная информация: ivalex.anna@gmail.com
GitHub: [профиль](https://github.com/IvalexAnna)
Github: [Яндекс Практикум](https://github.com/yandex-praktikum)
# Примеры запросов
Пример POST-запроса с токеном Антона Чехова: добавление нового поста.

*POST .../api/v1/posts/*
```JSON
{

    "text": "Вечером собрались в редакции «Русской мысли», чтобы поговорить о народном театре. Проект Шехтеля всем нравится.",

    "group": 1

}
```

Пример ответа:
```JSON
{

    "id": 14,

    "text": "Вечером собрались в редакции «Русской мысли», чтобы поговорить о народном театре. Проект Шехтеля всем нравится.",

    "author": "anton",

    "image": null,

    "group": 1,

    "pub_date": "2021-06-01T08:47:11.084589Z"

}
```

Пример POST-запроса с токеном Антона Чехова: отправляем новый комментарий к посту с `id=14`.

*POST .../api/v1/posts/14/comments/_*
```JSON
{

    "text": "тест тест"

}
```

Пример ответа:
```JSON
{

    "id": 4,

    "author": "anton",

    "post": 14,

    "text": "тест тест",

    "created": "2021-06-01T10:14:51.388932Z"

}
```

Пример GET-запроса с токеном Антона Чехова: получаем информацию о группе.

*GET.../api/v1/groups/2/_* 

Пример ответа:
```JSON
{

    "id": 2,

    "title": "Математика",

    "slug": "math",

    "description": "Посты на тему математики"

}
```
<a name="readme-top"></a>

<h3 align="center">Bewise тестовое задание 1</h3>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">О проекте</a>
      <ul>
        <li><a href="#built-with">Технологии</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Подкотовка и запуск</a>
      <ul>
        <li><a href="#prerequisites">Предварительные условия</a></li>
        <li><a href="#how-to-launch">Как запустить</a></li>
        <li><a href="#db-access">Как подключиться к СУБД</a></li> 
      </ul>
    </li>
    <li><a href="#usage">Использование</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
<a name="about-the-project"></a>
## О проекте
Данный сервис принимает POST-запрос с параметром "questions_num", содержащим количество вопросов, которые необходимо получить из публичного API.
После получения запроса, сервис выполняет запрос к публичному API по адресу https://jservice.io/api/random?count=<questions_num>, где <questions_num> - количество запрошенных вопросов.
Далее, полученные ответы сохраняются в базе данных.
В случае, если в БД имеется такой же вопрос, к публичному API с выполняются дополнительные запросы до тех пор, пока не будет получен уникальный вопрос
Ответом на запрос из будет предыдущей сохранённый вопрос. В случае его отсутствия вернется пустой объект.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<a name="built-with"></a>
### Технологии

Фреймворки и библиотеки 
* [![FastAPI][FastAPI]][FastAPI-url]
* [![SQLAlchemy][SQLAlchemy]][SQLAlchemy-url]
* [![Alembic][Alembic]][Alembic-url]
* [![Pydantic][Pydantic]][Pydantic-url]
* [![httpx][httpx]][httpx-url]

База данных а также средства контейнеризации
* [![Docker][Docker]][Docker-url]
* [![PostgreSQL][PostgreSQL]][PostgreSQL-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
<a name="getting-started"></a>
## Подготовка и запуск

<a name="prerequisites"></a>
### Предварительные условия
У вас должны быть установленны следущие приложения

* docker
* docker-compose


<a name="how-to-launch"></a>
### Как запустить

1. Скопируйте репозиторий
   ```sh
   git clone https://github.com/RezuanDzibov/bewise_test_1
   ```
2. Перейдите в директорию проекта

3. Переименуйте .env.template в .env следующей командой

    Windows 
    ```sh
     copy .env.template .env
    ```
   
    Linux/MacOS 
    ```sh
     cp .env.template .env
    ```

4. Запускаем
   ```sh
   docker-compose up --build
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a name="db-access"></a>
### Подключение к СУБД
После запуска проекта вам нужно находиться в корневой директори проекта

1. Получаем доступ к башу контейнера СУБД
   ```sh
   docker exec -it postgres_bewise_1 bash
   ```

2. Подключаемся к СУБД, вместо POSTGRES_USER надо подставить нужное значение из .env файла, по дефолту это bewise
   ```sh
   psql -U bewise
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
<a name="usage"></a>
## Примеры запросов

Если в БД нету записей

![no_questions_in_db]

Если в БД есть записи

![questions_in_db]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[no_questions_in_db]: images/no_questions_in_db.jpeg
[questions_in_db]: images/questions_in_db.jpeg
[FastAPI]: https://img.shields.io/badge/fastapi-05998b?style=for-the-badge&logo=fastapi&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com/
[SQLAlchemy]: https://img.shields.io/badge/sqlalchemy-778876?style=for-the-badge&logo=python&logoColor=black
[SQLAlchemy-url]: https://www.sqlalchemy.org/
[Alembic]: https://img.shields.io/badge/alembic-6ba81d?style=for-the-badge&logo=python&logoColor=black
[Alembic-url]: https://alembic.sqlalchemy.org/en/latest/
[Pydantic]: https://img.shields.io/badge/Pydantic-e92064?style=for-the-badge&logo=python&logoColor=black
[Pydantic-url]: https://docs.pydantic.dev/latest/
[httpx]: https://img.shields.io/badge/httpx-ffffff?style=for-the-badge&logo=python&logoColor=black
[httpx-url]: https://www.python-httpx.org/
[Docker]: https://img.shields.io/badge/Docker-230db7?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
[PostgreSQL]: https://img.shields.io/badge/PostgreSQL-233161?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/

### О проекте
Проект представляет собой веб-API, который хранит и возвращает случайные вопросы из сервиса jservice.io через. 
После запроса пользователя происходит сбора случайных вопросов c API jservice.io, сервис сохраняет их в базе данных и отвечвет последним сохраненным вопросом в базе данных. 


### Для запуска проекта выполните следующие шаги:
1. Скопируйте репозиторий: ```git clone https://github.com/RezuanDzibov/bewise_test_1/```
2. Перейдите в директорию c исходным кодом: ```cd bewise_test_1```
3. Переименуйте`.env.template` в `.env` следующей командой:

Windows
```copy .env.template .env```

Linux/MacOS
```cp .env.template .env```

4. Запускаем проект: ```docker-compose up --build```
5. Чтобы протестировать проект можно использовать интерфейс Swagger, перейдите по ссылке: http://127.0.0.1:8000/docs или curl-ом
```curl -X POST http://127.0.0.1:8000 -H 'Content-Type: application/json' -d '{"question_num": 1}'```

Желаю вам хорошего дня!

### About project

The project is a web API that stores and returns random questions from the jservice.io service. 
After a user request, the service collects random questions from the jservice.io API, stores them in a database, and responds with the last saved question in the database.

### To run the project, follow these steps:

1. Clone the repository: ```git clone https://github.com/RezuanDzibov/bewise_test_1/```
2. Navigate to the directory with the source code: ```cd bewise_test_1```
3. Rename ```.env.template``` to ```.env``` using the following command:

Windows
```copy .env.template .env```

Linux/MacOS
```cp .env.template .env```

4. Run the project: ```docker-compose up --build```
5. To test the project, you can use the Swagger interface by going to the following link: http://127.0.0.1:8000/docs
or use curl with the following command:
```curl -X POST http://127.0.0.1:8000 -H 'Content-Type: application/json' -d '{"question_num": 1}'```

Have a great day!
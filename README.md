### Starting the project

1. Clone it
   `git clone https://github.com/mrnosomebody/lms.git`
2. Create .env file in the project root `touch .env` containing this variables:

```
SECRET_KEY=<your_secret_here>
POSTGRES_DB=<your_db_name_here>
POSTGRES_USER=<your_db_user_here>
POSTGRES_PASSWORD=<your_db_password_here>
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

3. Start docker container
   ` sudo docker-compose up --build`

4. That's it. Go to the `localhost:8000/`. Database already contains some data, because I prepopulated it in custom
   migration
5. You can generate report by sending a `POST` request to `/reports/`. You will get task `uuid` in response. To download it send `GET` to `reports/download/<report_id>/`
6. To get status of the generating report send `GET` to `tasks/<uuid>/`.
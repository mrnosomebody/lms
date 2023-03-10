## Задание: Реализовать веб-сервис для организации учебного процесса в ВУЗе

### <u>Основные сущности</u>:

> 1. Куратор
> 2. Направление подготовки
> 3. Учебная дисциплина
> 4. Учебная группа
> 5. Студент

### Администратором 
#### сервиса формируются направления подготовки, имеющие свой перечень учебных дисциплин. За каждым направлением закреплен куратор. Куратор зачисляет студентов и формирует учебные группы на основании направлений. Каждая группа может состоять максимум из 20 студентов.


### <u>Функционал администратора</u>:
> 1. Управление направлениями подготовки
> 2. Управление учебными дисциплинами
> 3. Формирование отчета в виде эксель файла

### <u>Функционал куратора</u>:
> 1. Управление студентами
> 2. Управление учебными группами

## Требования:
> 1. Набор полей моделей на личное усмотрение.
> 2. Отчет администратора должен содержать в себе информацию о направлениях(список направлений и их дисциплин и данные кураторов) и о группах(отсортированный список студентов, данные о составе групп(кол-во мужчин и женщин, количество свободных мест в группе)).
> 3. Отчет должен генерироваться с помощью асинхронной задачи. Должен быть отдельный метод, позволяющий узнать статус задачи и сгенерированный отчет.
> 4. Весь проект должен быть покрыт автотестами(PyTest)
> 5. Весь проект должен пройти проверку mypy + Flake8

### <u>Стек</u>: 
- DRF
- PyTest
- СУБД PostgreSQL
- Celery для асинхронных задач, брокер на свой выбор.

### <u>Что будет оцениваться</u>:
> 1. Владение языком программирования и основными инструментами DRF(представления, сериализация, Django ORM, структуры данных)
> 2. Архитектурные решения(структура проекта в целом, структура приложения, разбиение на слои)
> 3. Общий подход к написанию кода: чистота и понятность кода, правильное разбиение логики, оформление кода, соответствие принципам и стандартам
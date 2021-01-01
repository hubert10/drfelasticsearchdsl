# Django Rest Framework Elasticsearch-dsl Example

This simple project explains how to integrate Django Rest API (Django Rest Framework) with Elasticsearch (Elasticsearch-dsl)
that automates the indexation and search of django models.

###### WARNING! This simple project is only for local testing, it's not prepared for deployment into remote server.

## Prerequisites

- Working Docker instance
- Docker-compose

## Getting Started

Steps to build, and run project:

1. `cd` to root of project
2. `docker-compose build`
3. `docker-compose up`
4. `docker-compose exec web python manage.py makemigrations`
5. `docker-compose exec web python manage.py migrate`
6. `docker-compose exec web python manage.py createsuperuser`
7. `Go the Admin Panel, add some skills, and start searching`

To test Elasticsearch on browser run these query: http://localhost:8000/searches/skills/:
If the list is empty, run these commands to create and index data:

1. `docker-compose exec web python manage.py search_index --create -f`
2. `docker-compose exec web python manage.py search_index --populate -f`

## Examples of usage

- http://localhost:8000/searches/skills/?search=django - search and display skills, which contain the word ‘django’ in the title.

## Links

Check out article to this project:
https://www.merixstudio.com/blog/elasticsearch-django-rest-framework/

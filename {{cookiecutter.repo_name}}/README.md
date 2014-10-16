{{ cookiecutter.project_name }}
======

Installation
------

1. Install PostgreSQL
> sudo apt-get install postgresql-server postgresql-dev
2. Create virtualenv
3. Install requirements
> pip install -r pip-req.txt
4. Create database
> sudo -u postgres createdb mydb
5. Migrate database
> ./manage.py migrate


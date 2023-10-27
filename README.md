# DjangoTaskManagement
Create a Jira like task management system with django

# Starting point
- Clone the repository locally to your system: `git clone https://github.com/ChristosHadjigeorghiou1996/DjangoTaskManagement.git`.
- Create virtual environment: `python -m venv VENV_NAME`
- Activate it with `.\VENV_NAME\Script\activate` or `source VENV_NAME/bin/activate` depending on OS
- Create project by typing: `django-admin startproject PROJECT_NAME`
- Start project by going to the project via `cd PROJECT_NAME` and `python manage.py runserver`
- Create an app via `python manage.py startapp BASE_NAME` and update it in PROJECT_NAME/settings.py

# Considerations
The fundamental principle is to store as minimal information as possible - cannot leak the data that is not there.

# Initial Database schema
Initial idea is to have user be able to create tasks, share them with colleagues and label tasks as not_started, started or finished.

![First version of database schema](src/db_schemas/database_schema_version_1.png)

# Final notes
This project is just a simple task management to get accustomed with django.

It is not created with the aim to duplicate / replace any existing software.
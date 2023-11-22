# DjangoTaskManagement
Create a Jira like task management system with django

# Starting point
- Clone the repository locally to your system: `git clone https://github.com/ChristosHadjigeorghiou1996/DjangoTaskManagement.git`.
- Create virtual environment: `python -m venv VENV_NAME`
- Activate it with `.\VENV_NAME\Script\activate` or `source VENV_NAME/bin/activate` depending on OS
- Install requirements.txt `pip install -r requirements.txt`
- Navigate to app folder and run `python manage.py test` to assert the correct installation of project.
- Create project by typing: `django-admin startproject PROJECT_NAME`
- Start project by going to the project via `cd PROJECT_NAME` and `python manage.py runserver`
- Run `python manage.py makemigrations` and `python manage.py migrate` to populate local db.

# Loading dummy data
- 'base/sample_data/sample_data.json' includes some dummy data to start/test the project.
- After running migrations, load them using `python manage.py loaddata base\sample_data\sample_data.json`

# Considerations
The fundamental principle is to store as minimal information as possible - cannot leak the data that is not there.

Enable users to create tasks and export / import them without having to register in.

# Initial Database schema
Initial idea is to have user be able to create tasks, share them with colleagues and label tasks as not_started, started or finished.

![First version of database schema](src/db_schemas/database_schema_version_1.png)


# Features
Initial view of home page with flash messages when dragging and dropping the tasks
![First version of home view](src/progress/flash%20messages.png)

Initial view of profile with option to go back using referer and if not request.user then tasks section becomes inaccessible
![image](https://github.com/ChristosHadjigeorghiou1996/DjangoTaskManagement/assets/87614879/a1e190d5-ff1c-414d-929b-d397b5612163)


# Final notes
This project is just a simple task management to get accustomed with django.

It is not created with the aim to duplicate / replace any existing software.

# Django Commands

Below is a list of common Django commands along with explanations and examples. These commands are used in the Django development process for various tasks such as creating projects, applications, running the development server, and managing database migrations.

1. **django-admin startproject:**
   - **Explanation:** Creates a new Django project.
   - **Example:** `django-admin startproject mysite`

2. **python manage.py runserver:**
   - **Explanation:** Starts the development server.
   - **Example:** `python manage.py runserver`

3. **python manage.py migrate:**
   - **Explanation:** Applies database migrations.
   - **Example:** `python manage.py migrate`

4. **python manage.py makemigrations:**
   - **Explanation:** Creates new database migrations based on changes in models.
   - **Example:** `python manage.py makemigrations`

5. **python manage.py createsuperuser:**
   - **Explanation:** Creates a superuser for the admin interface.
   - **Example:** `python manage.py createsuperuser`

6. **python manage.py startapp:**
   - **Explanation:** Creates a new Django application within a project.
   - **Example:** `python manage.py startapp myapp`

7. **python manage.py shell:**
   - **Explanation:** Opens the Django interactive shell for testing code.
   - **Example:** `python manage.py shell`

8. **python manage.py migrate --database=db_alias:**
   - **Explanation:** Applies migrations to a specific database defined in settings.
   - **Example:** `python manage.py migrate --database=my_database`

9. **python manage.py collectstatic:**
   - **Explanation:** Collects static files into the `STATIC_ROOT` directory.
   - **Example:** `python manage.py collectstatic`

10. **python manage.py showmigrations:**
    - **Explanation:** Displays a list of all migrations and their status.
    - **Example:** `python manage.py showmigrations`

11. **python manage.py test app_name:**
    - **Explanation:** Runs tests for a specific app.
    - **Example:** `python manage.py test myapp`

12. **python manage.py flush:**
    - **Explanation:** Resets the database by removing all data from it.
    - **Example:** `python manage.py flush`

13. **python manage.py dbshell:**
    - **Explanation:** Opens the database shell for the default database.
    - **Example:** `python manage.py dbshell`

14. **python manage.py check:**
    - **Explanation:** Checks for issues and inconsistencies in your project.
    - **Example:** `python manage.py check`

15. **python manage.py runserver 0.0.0.0:8000:**
    - **Explanation:** Starts the development server and makes it accessible externally.
    - **Example:** `python manage.py runserver 0.0.0.0:8000`

16. **python manage.py runserver_plus:**
    - **Explanation:** Starts the development server with additional Werkzeug features.
    - **Example:** `python manage.py runserver_plus`

17. **python manage.py dbshell --database=db_alias:**
    - **Explanation:** Opens the database shell for a specific database defined in settings.
    - **Example:** `python manage.py dbshell --database=my_database`

18. **python manage.py showmigrations app_name:**
    - **Explanation:** Displays a list of all migrations for a specific app.
    - **Example:** `python manage.py showmigrations myapp`

19. **python manage.py sqlmigrate app_name migration_name:**
    - **Explanation:** Displays the SQL statements for a specific migration.
    - **Example:** `python manage.py sqlmigrate myapp 0001`

20. **python manage.py check --deploy:**
    - **Explanation:** Checks for common issues in a deployment environment.
    - **Example:** `python manage.py check --deploy`

21. **python manage.py flush --noinput:**
    - **Explanation:** Resets the database without asking for confirmation.
    - **Example:** `python manage.py flush --noinput`

22. **python manage.py createsuperuser --username admin --email admin@example.com:**
    - **Explanation:** Creates a superuser with a specific username and email.
    - **Example:** `python manage.py createsuperuser --username admin --email admin@example.com`

23. **python manage.py changepassword username:**
    - **Explanation:** Changes the password for a specific user.
    - **Example:** `python manage.py changepassword john`

24. **python manage.py dbshell --command="SQL_COMMAND":**
    - **Explanation:** Executes a SQL command in the database shell.
    - **Example:** `python manage.py dbshell --command="SELECT * FROM mytable"`

25. **python manage.py runserver 8000:**
    - **Explanation:** Starts the development server on a specific port.
    - **Example:** `python manage.py runserver 8000`

26. **python manage.py dbshell --database=db_alias --command="SQL_COMMAND":**
    - **Explanation:** Executes a SQL command in the database shell for a specific database.
    - **Example:** `python manage.py dbshell --database=my_database --command="SELECT * FROM mytable"`

27. **python manage.py dbshell --database=db_alias --plain:**
    - **Explanation:** Opens the database shell in plain mode for a specific database.
    - **Example:** `python manage.py dbshell --database=my_database --plain`

28. **python manage.py runserver 0.0.0.0:8000 --insecure:**
    - **Explanation:** Starts the development server with insecure mode (no static files serving).
    - **Example:** `python manage.py runserver 0.0.0.0:8000 --insecure`

29. **python manage.py flush --noinput --database=db_alias:**
    - **Explanation:** Resets a specific database without asking for confirmation.
    - **Example:** `python manage.py flush --noinput --database=my_database`

30. **python manage.py makemigrations --empty app_name:**
    - **Explanation:** Creates an empty migration file for a specific app.
    - **Example:** `python manage.py makemigrations --empty myapp`

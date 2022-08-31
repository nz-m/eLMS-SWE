
# e-Learning Management System
A learning management and online assessment system for academic education.





## Features

- Admin adds courses, teachers, and students and assigns them courses.
- The teacher creates course content, announcements, assignments, quizzes, takes attendance, etc. A teacher can see the details and analysis of the assessments.
- Students can enroll in the courses using the access key, see the course content of the enrolled courses, participate in assessments and see their results in detail.
- Discussion section for both teacher and student.

## Tech Stack
1. Django 4.0.4
2. Bootstrap 5.0.2
3. jQuery 3.6.0
5. Chart.js v3.9.1
4. Animate.css 4.1.1


## Run Locally

1. Clone the project
```bash
  git clone https://github.com/nz-m/eLMS-SWE.git
```
2. Go to the project directory
```bash
  cd eLMS-SWE
```
3. Create a virtual environment and activate it (Windows)
```bash
  python -m venv env
```
```bash
  env\Scripts\activate
```
4. Install dependencies

```bash
  pip install -r requirements.txt
```
5. Make migrations and migrate
```bash
  python manage.py makemigrations
```
```bash
  python manage.py migrate
```
6. Create admin/superuser
```bash
  python manage.py createsuperuser
```
7. Finally run the project
```bash
  python manage.py runserver
```
Now the project should be running on http://127.0.0.1:8000/

Login as admin and add some courses, teacher and students.


## License
[The MIT License (MIT)](https://github.com/nz-m/eLMS-SWE/blob/main/LICENCE)



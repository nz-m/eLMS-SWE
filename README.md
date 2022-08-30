
# e-Learning Management System
A learning management and online assessment system for academic education.





## Features

- Admin adds courses, teacher, student and assign them courses.
- Teacher creates course content, announcements, assignments, quizzes, takes attendance etc. Teacher can see the details and analysis of the assessments.
- Student can enroll in course usign access key, see course content of the enrolled courses, participate in assessments and see their results in details.
- Discussion section for both teacher and student.



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



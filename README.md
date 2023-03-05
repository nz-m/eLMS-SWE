# e-Learning Management System

A learning management and online assessment system for academic education.

## Features

- Admin adds courses, teachers, and students and assigns them courses.
- The teacher creates course content, announcements, assignments, quizzes, takes attendance, etc. A teacher can see the details and analysis of the assessments.
- Students can enroll in the courses using the access key, see the course content of the enrolled courses, participate in assessments and see their results in detail.
- Discussion section for both teacher and student.

## Relational Schema

![schema](https://user-images.githubusercontent.com/87283264/187967219-55bea00e-3151-488a-a4be-d2a95b9d8a5c.png)

## Tech Stack

1. Django 4.0.4
2. Bootstrap 5.0.2
3. jQuery 3.6.0
4. Chart.js v3.9.1
5. Animate.css 4.1.1

## UI

![Screenshot (65)](https://user-images.githubusercontent.com/87283264/194387627-47bc4506-5acb-46da-8ae0-70ea1e7e4eb8.png)
![Screenshot (63)](https://user-images.githubusercontent.com/87283264/194389617-1d1118a5-e0a1-41a2-94b6-ef636e6a8d5e.png)
![Screenshot (70)](https://user-images.githubusercontent.com/87283264/194387776-552bdd11-9252-4be2-8139-10e0f270c09f.png)
![Screenshot (71)](https://user-images.githubusercontent.com/87283264/194389301-da1f2cd5-11fd-469d-9137-380c4916e169.png)
![Screenshot (72)](https://user-images.githubusercontent.com/87283264/194389315-c59fbae1-b623-4ef7-bc5b-7cab6c1ae3a8.png)
![Screenshot (67)](https://user-images.githubusercontent.com/87283264/194387798-77c6ba2c-9089-4469-88e0-282191535211.png)
![Screenshot (68)](https://user-images.githubusercontent.com/87283264/194387811-bd22cd8c-854c-4849-9aa9-0a71b53494a2.png)
![Screenshot (69)](https://user-images.githubusercontent.com/87283264/194387822-649bd890-cb57-47b5-b380-4e30499ae142.png)

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

> **Note:** If you're using newer versions of python(3.10+), you may need to add the `--use-deprecated=legacy-resolver` option when installing dependencies with `pip` to avoid errors :

```bash
pip install -r requirements.txt --use-deprecated=legacy-resolver
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

Demo : https://youtu.be/NyL2ajUNxYk

## License

[The MIT License (MIT)](https://github.com/nz-m/eLMS-SWE/blob/main/LICENCE)

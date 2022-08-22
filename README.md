# e-Learning Management System - SWE Lab(Summer-22)

## Installation

1. Clone the repository

```bash
git clone https://github.com/nz-m/eLMS-SWE.git
```

2. Create a virtual environment

```bash
py -m venv env
```

```bash
env\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```
4. Set up the database

```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
5. Create a superuser

```bash
python manage.py createsuperuser
```
6. Run the application

```bash
python manage.py runserver
```

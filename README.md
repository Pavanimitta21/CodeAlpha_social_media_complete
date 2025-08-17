Generated on 2025-08-17T10:08:40.626402 - Run:

python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

Open http://127.0.0.1:8000

# Project Manager 

#Project Overview

* Admin Theme integeration
* User Registeration and Login
* User Management 
* Roles and Permission Management
* Projects Management
* Projects details were encrypted in DB for security reason
* Dynamic Page titles using custom template view context processors
* Breadcrumbs

Project Setup 

* git clone repo
* python3 -m venv venv 
* source venv/bin/activate
* pip install -r requirements.txt
* source venv/bin/activate
* copy env.example in backend folder make .env file in backend
* python3 manage.py generate_encryption_key
* Copy the key and paste it after "SECRET_KEY=" of env
* python3 manage.py migrate
* Python3 manage.py collectstatic (to build static files like rpm run dev)
* python3 manage.py runserver

Email : admin@admin.com
Password : 123456

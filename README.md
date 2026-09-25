# Django Todo App

A Todo Management Application built with **Django** that allows users to create, view, update, and delete their personal tasks.

## 🌐 Live Demo

🚀 **Live Application:**  
http://51.21.194.230:8000/

> The application is deployed on an AWS EC2 server.

## 🚀 Features

* User Registration
* User Login and Logout
* Authentication using Django's built-in authentication system
* Create Todo
* View Todo List
* Update Todo
* Delete Todo
* Mark Todo as completed
* User-specific Todos
* Class-Based Views (CBVs)
* Login protection using `LoginRequiredMixin`
* Pagination
* SQLite database
* Bootstrap-based UI

## 🛠️ Technologies Used

* Python
* Django
* SQLite
* HTML
* CSS
* Bootstrap
* Git & GitHub
* AWS EC2

## 📁 Project Structure

```text
django-todo-app/
│
├── manage.py
├── db.sqlite3
│
├── project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── todos/
│   ├── migrations/
│   │   └── ...
│   ├── templates/
│   │   └── ...
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   ├── registration/
│   │   └── ...
│   └── ...
│
├── .gitignore
├── requirements.txt
└── README.md

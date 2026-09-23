# Django Todo App

A Todo Management Application built with **Django** that allows users to create, view, update, and delete their personal tasks.

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
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   ├── registration/
│   └── ...
│
├── .gitignore
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Sanyam9804/django-todo-app.git
```

### 2. Go into the project directory

```bash
cd django-todo-app
```

### 3. Create a virtual environment

```bash
python3 -m venv .venv
```

### 4. Activate the virtual environment

#### macOS / Linux

```bash
source .venv/bin/activate
```

#### Windows

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run migrations

```bash
python3 manage.py migrate
```

### 7. Start the development server

```bash
python3 manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## 🔐 Authentication

The application provides:

* Signup
* Login
* Logout
* Protected Todo dashboard
* User-specific Todo data

Users must be authenticated to access their Todo dashboard.

## 📌 Main Django Concepts Used

This project demonstrates several important Django concepts:

* Models
* Forms
* ModelForms
* URL routing
* Templates
* Django Authentication
* Class-Based Views
* `LoginRequiredMixin`
* `ListView`
* `CreateView`
* `UpdateView`
* `DeleteView`
* `reverse_lazy()`
* `get_object_or_404()`
* Pagination
* Django ORM
* SQLite
* Template inheritance

## 📄 Example Todo Flow

```text
User
 │
 ├── Signup
 │
 ├── Login
 │
 ▼
Todo Dashboard
 │
 ├── Create Todo
 │
 ├── View Todos
 │
 ├── Update Todo
 │
 ├── Delete Todo
 │
 └── Mark Complete
 │
 ▼
Logout
```

## 📦 Requirements

Example `requirements.txt`:

```text
asgiref==3.12.1
Django==6.1.1
sqlparse==0.6.0
```

Install them with:

```bash
pip install -r requirements.txt
```

## 🔮 Future Improvements

* Todo categories
* Due dates
* Search and filtering
* Priority levels
* REST API using Django REST Framework
* PostgreSQL database
* User profile
* Deployment to AWS
* Docker support

## 👨‍💻 Author

**Sanyam Kothari**

GitHub: [Sanyam9804](https://github.com/Sanyam9804)

## 📜 License

This project is created for learning and development purposes.

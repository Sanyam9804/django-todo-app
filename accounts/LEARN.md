# Django Authentication + CBV Cheat Sheet

## 1. Important Imports

| Import               | Type     | Use                                  |
| -------------------- | -------- | ------------------------------------ |
| `login`              | Function | Logs a user into the session         |
| `logout`             | Function | Logs a user out                      |
| `LoginView`          | CBV      | Built-in login page + authentication |
| `LogoutView`         | CBV      | Built-in logout                      |
| `TemplateView`       | CBV      | Render an HTML template              |
| `FormView`           | CBV      | Handle forms                         |
| `reverse_lazy()`     | Function | Resolve URL name → URL later         |
| `LoginRequiredMixin` | Mixin    | Restrict a CBV to logged-in users    |

---

# 2. TemplateView

```python
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "home.html"
```

### `template_name`

Specifies the HTML template.

```python
template_name = "home.html"
```

---

# 3. FormView

```python
from django.views.generic import FormView

class SignupView(FormView):
    template_name = "signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("todo_dashboard")
```

### Important attributes

| Attribute       | Meaning                              |
| --------------- | ------------------------------------ |
| `template_name` | Template to display                  |
| `form_class`    | Form class to use                    |
| `success_url`   | Redirect after successful submission |

### Important methods

| Method              | Called when             |
| ------------------- | ----------------------- |
| `form_valid()`      | Form is valid           |
| `form_invalid()`    | Form is invalid         |
| `get_success_url()` | Determines redirect URL |

---

# 4. `form_valid()`

```python
def form_valid(self, form):
    user = form.save()
    login(self.request, user)
    return super().form_valid(form)
```

Flow:

```text
POST
 ↓
form.is_valid()
 ↓
form_valid()
 ↓
form.save()
 ↓
login()
 ↓
super().form_valid()
 ↓
success_url
```

---

# 5. LoginView

Django's built-in login CBV.

```python
from django.contrib.auth.views import LoginView

class UserLoginView(LoginView):
    template_name = "login.html"
```

Django handles:

```text
Username
Password
   ↓
Authentication
   ↓
Session
   ↓
Login
```

### Useful attributes

| Attribute                     | Use                              |
| ----------------------------- | -------------------------------- |
| `template_name`               | Login template                   |
| `redirect_authenticated_user` | Redirect already logged-in users |
| `next_page`                   | Redirect after login             |
| `redirect_field_name`         | Name of the `next` parameter     |

Example:

```python
class UserLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True
```

---

# 6. `get_success_url()`

Used to decide where the user goes after successful login.

```python
def get_success_url(self):
    return reverse_lazy("todo_dashboard")
```

Can also be dynamic:

```python
def get_success_url(self):
    if self.request.user.is_staff:
        return reverse_lazy("admin_dashboard")

    return reverse_lazy("todo_dashboard")
```

---

# 7. LogoutView

Django's built-in logout CBV.

```python
from django.contrib.auth.views import LogoutView

class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")
```

Flow:

```text
Logout request
     ↓
Session removed
     ↓
Redirect
     ↓
Home
```

### Important attributes

| Attribute             | Use                                   |
| --------------------- | ------------------------------------- |
| `next_page`           | Redirect after logout                 |
| `template_name`       | Template if confirmation page is used |
| `redirect_field_name` | Redirect parameter                    |

---

# 8. `login()`

```python
from django.contrib.auth import login

login(request, user)
```

Purpose:

> Authenticate the user and store the user's ID in the session.

Example:

```python
user = form.save()
login(self.request, user)
```

After login:

```python
request.user
```

represents the logged-in user.

---

# 9. `reverse_lazy()`

```python
reverse_lazy("todo_dashboard")
```

Converts:

```text
URL name
   ↓
actual URL
```

Example:

```python
path(
    "todos/",
    TodoDashboardView.as_view(),
    name="todo_dashboard"
)
```

Then:

```python
reverse_lazy("todo_dashboard")
```

resolves to:

```text
/todos/
```

### Why `lazy`?

It waits until the URL is actually needed.

Useful in class attributes:

```python
success_url = reverse_lazy("todo_dashboard")
```

---

# 10. `super()`

```python
return super().form_valid(form)
```

Means:

> Call the parent class's version of `form_valid()`.

Example:

```text
SignupView
    ↓ inherits
FormView
```

So:

```python
super().form_valid(form)
```

calls:

```python
FormView.form_valid(form)
```

---

# 11. `LoginRequiredMixin`

Used to protect CBVs.

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    login_url = "login"
```

Flow:

```text
User visits /dashboard/
        ↓
Is logged in?
   ↙           ↘
 YES            NO
 ↓               ↓
Dashboard      Login
```

### Important attributes

```python
login_url = "login"
```

Where unauthenticated users are sent.

---

# 12. URL Configuration

```python
from django.urls import path

urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    path("signup/", SignupView.as_view(), name="signup"),

    path("login/", UserLoginView.as_view(), name="login"),

    path("logout/", UserLogoutView.as_view(), name="logout"),

    path(
        "todos/",
        TodoDashboardView.as_view(),
        name="todo_dashboard"
    ),
]
```

### Important CBV rule

```python
HomeView.as_view()
```

NOT:

```python
HomeView()
```

`as_view()` converts the class into a callable view function that Django's URL system can use.

---

# 13. Complete Authentication Flow

```text
                    HOME
                      │
          ┌───────────┴───────────┐
          ↓                       ↓
       SIGNUP                    LOGIN
          │                       │
          ↓                       ↓
     SignupForm              LoginView
          │                       │
          ↓                       ↓
      form_valid()           Authentication
          │                       │
          ↓                       ↓
      form.save()                login
          │                       │
          └───────────┬───────────┘
                      ↓
                 DASHBOARD
                      │
                LoginRequiredMixin
                      │
                      ↓
                    TODOS
                      │
                      ↓
                   LOGOUT
                      │
                      ↓
                    HOME
```

---

# 14. Attribute vs Method vs Function

This distinction is important.

### Attribute

```python
template_name = "login.html"
```

```python
form_class = SignupForm
```

```python
success_url = reverse_lazy("todo_dashboard")
```

---

### Method

```python
def form_valid(self, form):
```

```python
def get_success_url(self):
```

---

### Function

```python
login(self.request, user)
```

```python
reverse_lazy("home")
```

---

### Class

```python
LoginView
FormView
TemplateView
LogoutView
```

---

# 15. Your Code — Categorized

```python
from django.contrib.auth import login
# FUNCTION

from django.contrib.auth.views import LoginView, LogoutView
# CLASSES

from django.urls import reverse_lazy
# FUNCTION

from django.views.generic import TemplateView, FormView
# CLASSES

from .forms import SignupForm
# YOUR CUSTOM CLASS
```

```python
class HomeView(TemplateView):
    template_name = "home.html"
```

* `HomeView` → your class
* `TemplateView` → Django class
* `template_name` → Django attribute

---

```python
class SignupView(FormView):
    template_name = "signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("todo_dashboard")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
```

* `FormView` → Django class
* `template_name` → attribute
* `form_class` → attribute
* `success_url` → attribute
* `form_valid()` → Django method overridden by you
* `form.save()` → form method
* `login()` → Django function
* `super()` → Python feature

---

# 16. Most Important Things to Remember

```text
TemplateView
→ Render template

FormView
→ Handle forms

LoginView
→ Login

LogoutView
→ Logout

LoginRequiredMixin
→ Protect CBV

login()
→ Log user in

reverse_lazy()
→ URL name → URL later

form_valid()
→ Runs when form is valid

form_invalid()
→ Runs when form is invalid

get_success_url()
→ Decide redirect URL

success_url
→ Fixed redirect URL

as_view()
→ CBV → callable view for URL
```

## One-line memory trick

```text
TemplateView = Template

FormView = Form

LoginView = Login

LogoutView = Logout

LoginRequiredMixin = Protection

reverse_lazy = URL

form_valid = Success form processing

get_success_url = Where to go next
```

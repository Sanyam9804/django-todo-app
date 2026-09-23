# Django Class-Based Views (CBV)

## Cheat Sheet + Short Theory

---

# 1. What is CBV?

**Class-Based View (CBV)** means writing Django views using Python classes instead of functions.

### Function-Based View

```python
def todo_list(request):
    todos = Todo.objects.all()

    return render(
        request,
        "dashboard.html",
        {"todos": todos}
    )
```

### Class-Based View

```python
class TodoListView(ListView):
    model = Todo
    template_name = "dashboard.html"
```

### Why CBV?

Django provides built-in generic views that already contain common logic.

```text
ListView    → List objects
DetailView  → Show one object
CreateView  → Create object
UpdateView  → Update object
DeleteView  → Delete object
```

---

# 2. Most Important Generic CBVs

| CBV            | Purpose                  |
| -------------- | ------------------------ |
| `View`         | Base/custom view         |
| `TemplateView` | Render a template        |
| `ListView`     | Display multiple objects |
| `DetailView`   | Display one object       |
| `CreateView`   | Create object            |
| `UpdateView`   | Update object            |
| `DeleteView`   | Delete object            |
| `FormView`     | Work with a form         |
| `RedirectView` | Redirect to another URL  |

### Easy Memory

```text
List    → READ MANY
Detail  → READ ONE
Create  → CREATE
Update  → UPDATE
Delete  → DELETE
```

---

# 3. Basic `ListView`

```python
from django.views.generic import ListView
from .models import Todo


class TodoListView(ListView):

    model = Todo

    template_name = "todos/dashboard.html"

    context_object_name = "todos"
```

### Theory

`ListView` automatically retrieves objects from the specified model and sends them to the template.

---

# 4. `model`

```python
model = Todo
```

Tells the generic view:

> Which model should I work with?

```text
ListView
   ↓
Todo model
   ↓
Todo objects
```

---

# 5. `template_name`

```python
template_name = "todos/dashboard.html"
```

Specifies the HTML template that should be rendered.

---

# 6. `context_object_name`

```python
context_object_name = "todos"
```

Defines the variable name available in the template.

Without custom name:

```django
{{ object_list }}
```

With:

```python
context_object_name = "todos"
```

Use:

```django
{% for todo in todos %}
    {{ todo.title }}
{% endfor %}
```

---

# 7. `ListView` Default Flow

```text
Request
   ↓
ListView
   ↓
Get QuerySet
   ↓
Add objects to context
   ↓
Render template
```

---

# 8. `get_queryset()`

One of the most important CBV methods.

```python
def get_queryset(self):

    return Todo.objects.filter(
        user=self.request.user
    )
```

### Theory

`get_queryset()` controls **which database objects the view works with**.

Example:

```python
Todo.objects.all()
```

means:

```text
All Todos
```

But:

```python
Todo.objects.filter(
    user=self.request.user
)
```

means:

```text
Only current user's Todos
```

### Remember

```text
get_queryset()
       ↓
"What objects should this view use?"
```

---

# 9. `QuerySet`

A QuerySet represents a collection of database records.

Example:

```python
todos = Todo.objects.all()
```

```python
todos = Todo.objects.filter(
    completed=False
)
```

You can chain filters:

```python
todos = Todo.objects.filter(
    user=request.user
).filter(
    completed=False
)
```

---

# 10. `filter()`

```python
Todo.objects.filter(completed=False)
```

Returns objects matching the condition.

Examples:

```python
Todo.objects.filter(priority="high")
```

```python
Todo.objects.filter(completed=True)
```

```python
Todo.objects.filter(
    user=request.user,
    completed=False
)
```

### Memory

```text
filter() → multiple matching objects
```

---

# 11. `get()`

```python
Todo.objects.get(pk=1)
```

Used when you expect **one object**.

If object doesn't exist:

```text
DoesNotExist
```

If multiple objects match:

```text
MultipleObjectsReturned
```

---

# 12. `get_object_or_404()`

```python
from django.shortcuts import get_object_or_404


todo = get_object_or_404(
    Todo,
    pk=pk
)
```

### Theory

It tries to retrieve one object.

If found:

```text
Return object
```

If not found:

```text
HTTP 404
```

Conceptually:

```python
try:
    todo = Todo.objects.get(pk=pk)

except Todo.DoesNotExist:
    raise Http404
```

### Memory

```text
get()               → object / exception
get_object_or_404() → object / 404 page
```

---

# 13. `pk`

`pk` means **Primary Key**.

Example database:

```text
id    title
----------------
1     Learn Python
2     Learn Django
3     Learn DRF
```

Here:

```text
pk = id
```

URL:

```python
path(
    "todos/<int:pk>/",
    TodoDetailView.as_view()
)
```

URL:

```text
/todos/2/
```

means:

```python
pk = 2
```

---

# 14. `self`

Inside a class method:

```python
def get_queryset(self):
```

`self` represents the current object/instance of the class.

Example:

```python
self.request
```

means:

> Current request associated with this view.

---

# 15. `self.request`

Represents the current HTTP request.

Common properties:

```python
self.request.user
self.request.GET
self.request.POST
self.request.method
```

---

# 16. `request.user`

```python
self.request.user
```

Represents the currently logged-in user.

Example:

```python
Todo.objects.filter(
    user=self.request.user
)
```

This is commonly used to ensure users access only their own records.

---

# 17. `request.GET`

Contains URL query parameters.

URL:

```text
/todos/?status=pending
```

Code:

```python
status = self.request.GET.get("status")
```

Result:

```text
pending
```

Multiple parameters:

```text
/todos/?status=pending&priority=high
```

```python
status = request.GET.get("status")
priority = request.GET.get("priority")
```

---

# 18. `.get()`

```python
request.GET.get("status")
```

Retrieves a value safely.

If parameter doesn't exist:

```python
None
```

Compare:

```python
request.GET["status"]
```

This can raise:

```text
KeyError
```

if the key doesn't exist.

---

# 19. `paginate_by`

```python
class TodoListView(ListView):

    model = Todo

    paginate_by = 5
```

Means:

> Show 5 objects per page.

Example:

```text
10 Todos

Page 1 → 1-5
Page 2 → 6-10
```

Django automatically provides:

```django
page_obj
paginator
is_paginated
```

---

# 20. Pagination Variables

### `page_obj`

Represents the current page.

```django
{{ page_obj.number }}
```

Current page number.

### `paginator`

Represents the paginator.

```django
{{ page_obj.paginator.num_pages }}
```

Total pages.

### `is_paginated`

Checks whether pagination is being used.

```django
{% if is_paginated %}
```

---

# 21. `get_context_data()`

```python
def get_context_data(self, **kwargs):

    context = super().get_context_data(**kwargs)

    context["total_count"] = 10

    return context
```

### Theory

Used to add **extra data** to the template context.

```text
get_queryset()
      ↓
Which objects?

get_context_data()
      ↓
What extra information?
```

Example:

```python
context["total_count"] = all_todos.count()
context["completed_count"] = completed_count
context["pending_count"] = pending_count
```

Template:

```django
{{ total_count }}
{{ completed_count }}
{{ pending_count }}
```

---

# 22. `super()`

```python
super().get_context_data(**kwargs)
```

Calls the parent class's implementation.

Example:

```text
TodoListView
     ↓
ListView
     ↓
View
```

Therefore:

```python
super().get_context_data()
```

calls the `ListView` implementation before adding your custom data.

### Memory

```text
super()
   ↓
"Use parent's implementation"
```

---

# 23. `**kwargs`

```python
def get_context_data(self, **kwargs):
```

`**kwargs` means the function can accept additional keyword arguments.

You commonly see it in Django CBV methods.

---

# 24. `CreateView`

```python
class TodoCreateView(LoginRequiredMixin, CreateView):

    model = Todo

    fields = [
        "title",
        "description",
        "priority"
    ]

    template_name = "todos/todo_form.html"

    success_url = reverse_lazy("todo_dashboard")
```

### Theory

`CreateView` handles the common process of creating a model object.

```text
Display Form
     ↓
User submits
     ↓
Validate
     ↓
Save
     ↓
Redirect
```

---

# 25. `fields`

```python
fields = [
    "title",
    "description",
    "priority"
]
```

Defines which model fields should appear in the generated form.

Example:

```python
class Todo(models.Model):

    title = models.CharField(...)
    description = models.TextField(...)
    priority = models.CharField(...)
    completed = models.BooleanField(...)
```

If:

```python
fields = [
    "title",
    "description",
    "priority"
]
```

then `completed` isn't included in the form.

---

# 26. `form_valid()`

```python
def form_valid(self, form):

    form.instance.user = self.request.user

    return super().form_valid(form)
```

Called after the form passes validation.

### Flow

```text
Submit form
    ↓
Validate
    ↓
Valid
    ↓
form_valid()
    ↓
Save
```

---

# 27. `form.instance`

```python
form.instance
```

Represents the model object that the form is going to save.

Example:

```python
form.instance.user = self.request.user
```

means:

> Assign the current user to this Todo before saving it.

---

# 28. Why `form.instance.user`?

Suppose:

```python
class Todo(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )
```

But your form has:

```python
fields = [
    "title",
    "description",
    "priority"
]
```

`user` isn't entered by the user.

So you assign it programmatically:

```python
form.instance.user = self.request.user
```

---

# 29. `UpdateView`

```python
class TodoUpdateView(LoginRequiredMixin, UpdateView):

    model = Todo

    fields = [
        "title",
        "description",
        "priority"
    ]

    template_name = "todos/todo_form.html"

    success_url = reverse_lazy("todo_dashboard")
```

### Theory

`UpdateView` is used to edit an existing object.

```text
Existing Todo
     ↓
Load object
     ↓
Display form
     ↓
Edit
     ↓
Validate
     ↓
Update database
     ↓
Redirect
```

---

# 30. `DeleteView`

```python
class TodoDeleteView(LoginRequiredMixin, DeleteView):

    model = Todo

    template_name = "todos/todo_confirm_delete.html"

    success_url = reverse_lazy("todo_dashboard")
```

### Theory

`DeleteView` handles object deletion.

```text
Object
  ↓
Confirmation
  ↓
DELETE
  ↓
Redirect
```

---

# 31. `LoginRequiredMixin`

```python
class TodoListView(
    LoginRequiredMixin,
    ListView
):
```

Ensures that the user must be authenticated.

If not:

```text
/todos/
   ↓
/login/
```

Set the login URL:

```python
login_url = reverse_lazy("login")
```

### Important

Put the mixin **before** the generic view:

```python
LoginRequiredMixin, ListView
```

not:

```python
ListView, LoginRequiredMixin
```

---

# 32. `reverse_lazy()`

```python
reverse_lazy("login")
```

Converts a URL name into its URL.

Given:

```python
path(
    "login/",
    LoginView.as_view(),
    name="login"
)
```

Then:

```python
reverse_lazy("login")
```

resolves to:

```text
/login/
```

Common usage:

```python
login_url = reverse_lazy("login")

success_url = reverse_lazy("todo_dashboard")
```

---

# 33. `success_url`

```python
success_url = reverse_lazy("todo_dashboard")
```

Defines where the user goes after successful operation.

Example:

```text
Create Todo
    ↓
Save
    ↓
success_url
    ↓
Dashboard
```

---

# 34. `View`

```python
class TodoToggleView(
    LoginRequiredMixin,
    View
):
```

`View` is the basic Django CBV.

You define the HTTP behavior yourself.

Example:

```python
class TodoToggleView(View):

    def post(self, request, pk):
        ...
```

Common methods:

```python
def get(self, request):
    ...

def post(self, request):
    ...

def put(self, request):
    ...

def delete(self, request):
    ...
```

---

# 35. HTTP Methods in CBV

| Method   | Common Purpose   |
| -------- | ---------------- |
| `GET`    | Retrieve/display |
| `POST`   | Create/submit    |
| `PUT`    | Replace/update   |
| `PATCH`  | Partial update   |
| `DELETE` | Delete           |

In Django:

```python
def get(self, request):
```

handles GET.

```python
def post(self, request):
```

handles POST.

---

# 36. Toggle Example

```python
class TodoToggleView(LoginRequiredMixin, View):

    login_url = reverse_lazy("login")

    def post(self, request, pk):

        todo = get_object_or_404(
            Todo,
            pk=pk,
            user=request.user
        )

        todo.completed = not todo.completed

        todo.save()

        return redirect("todo_dashboard")
```

Flow:

```text
POST
 ↓
Find Todo
 ↓
Check owner
 ↓
Toggle completed
 ↓
Save
 ↓
Redirect
```

---

# 37. `not`

```python
todo.completed = not todo.completed
```

Boolean inversion.

```text
False → True
True  → False
```

Useful for toggle functionality.

---

# 38. `save()`

```python
todo.save()
```

Saves the current model instance to the database.

Example:

```python
todo.completed = True
todo.save()
```

Flow:

```text
Python object
     ↓
Change
     ↓
save()
     ↓
Database
```

---

# 39. `redirect()`

```python
return redirect("todo_dashboard")
```

Redirects the browser to a named URL.

Example:

```python
path(
    "todos/",
    TodoListView.as_view(),
    name="todo_dashboard"
)
```

Then:

```python
redirect("todo_dashboard")
```

goes to:

```text
/todos/
```

---

# 40. `as_view()`

Very important for CBVs.

In `urls.py`:

```python
path(
    "todos/",
    TodoListView.as_view(),
    name="todo_dashboard"
)
```

`TodoListView` is a class.

`as_view()` converts the class into a callable view that Django's URL system can use.

```text
TodoListView
     ↓
as_view()
     ↓
Callable View
     ↓
Django URL
```

---

# 41. `get_queryset()` vs `get_context_data()`

This is a common interview question.

| Method               | Purpose                   |
| -------------------- | ------------------------- |
| `get_queryset()`     | Controls database objects |
| `get_context_data()` | Adds extra template data  |

Example:

```python
def get_queryset(self):

    return Todo.objects.filter(
        user=self.request.user
    )
```

Means:

> Which Todos?

While:

```python
def get_context_data(self, **kwargs):

    context = super().get_context_data(**kwargs)

    context["total_count"] = 10

    return context
```

Means:

> What additional data should the template receive?

---

# 42. `get()` vs `filter()` vs `get_object_or_404()`

| Method                | Result                      |
| --------------------- | --------------------------- |
| `get()`               | One object                  |
| `filter()`            | QuerySet / multiple objects |
| `get_object_or_404()` | One object or HTTP 404      |

Example:

```python
Todo.objects.get(pk=1)
```

```python
Todo.objects.filter(user=request.user)
```

```python
get_object_or_404(
    Todo,
    pk=1
)
```

---

# 43. `get_queryset()` Security Pattern

For user-specific data:

```python
def get_queryset(self):

    return Todo.objects.filter(
        user=self.request.user
    )
```

This is important for:

```text
UpdateView
DeleteView
ListView
```

It prevents users from accessing another user's records through predictable IDs.

---

# 44. Complete CRUD Mental Model

```text
                 CRUD
                  │
       ┌──────────┼──────────┐
       │          │          │
      READ       CREATE    UPDATE
       │          │          │
   ListView    CreateView UpdateView
       │          │          │
       │          │          │
       └──────────┼──────────┘
                  │
              Delete
                  │
             DeleteView
```

---

# 45. CBV Method Cheat Sheet

```text
get_queryset()
    → Which objects?

get_context_data()
    → What extra template data?

form_valid()
    → What happens after form validation?

form_invalid()
    → What happens when form validation fails?

get()
    → Handle GET request

post()
    → Handle POST request

dispatch()
    → Routes request to get/post/etc.

as_view()
    → Converts class into callable view
```

---

# 46. Important Attributes

```python
model
```

Which model?

```python
template_name
```

Which template?

```python
fields
```

Which form fields?

```python
context_object_name
```

What variable name in template?

```python
success_url
```

Where to redirect after success?

```python
login_url
```

Where to redirect unauthenticated users?

```python
paginate_by
```

How many objects per page?

---

# 47. Your Todo App — Complete Structure

```text
TodoListView
     │
     ├── LoginRequiredMixin
     │
     ├── model = Todo
     │
     ├── template_name
     │
     ├── context_object_name
     │
     ├── paginate_by
     │
     ├── get_queryset()
     │       ├── user filter
     │       ├── status filter
     │       └── priority filter
     │
     └── get_context_data()
             ├── total_count
             ├── completed_count
             └── pending_count


TodoCreateView
     │
     ├── CreateView
     ├── fields
     ├── form_valid()
     │       └── assign user
     └── success_url


TodoUpdateView
     │
     ├── UpdateView
     ├── fields
     ├── get_queryset()
     │       └── current user only
     └── success_url


TodoDeleteView
     │
     ├── DeleteView
     ├── get_queryset()
     │       └── current user only
     └── success_url


TodoToggleView
     │
     ├── View
     ├── post()
     ├── get_object_or_404()
     ├── toggle completed
     ├── save()
     └── redirect()
```

---

# 48. Quick Interview Cheat Sheet

### What is CBV?

> A Django view implemented using a Python class.

### What is `ListView`?

> Generic CBV for displaying a list of objects.

### What is `CreateView`?

> Generic CBV for creating objects through a form.

### What is `UpdateView`?

> Generic CBV for updating an existing object.

### What is `DeleteView`?

> Generic CBV for deleting an object.

### What is `get_queryset()`?

> Controls the objects returned/used by the view.

### What is `get_context_data()`?

> Adds additional data to the template context.

### What is `form_valid()`?

> Executes when a submitted form passes validation.

### What is `LoginRequiredMixin`?

> Restricts a view to authenticated users.

### What is `reverse_lazy()`?

> Lazily resolves a named URL.

### What is `get_object_or_404()`?

> Retrieves an object or returns HTTP 404.

### What is `as_view()`?

> Converts a CBV class into a callable view.

### What is `pk`?

> Primary key of an object.

### What is `paginate_by`?

> Number of objects displayed per page.

---

# 49. 30-Second Revision

```text
CBV
│
├── View
│
├── ListView      → List
├── DetailView    → One object
├── CreateView    → Create
├── UpdateView    → Update
└── DeleteView    → Delete


Important attributes
│
├── model
├── template_name
├── fields
├── context_object_name
├── success_url
├── login_url
└── paginate_by


Important methods
│
├── get_queryset()
├── get_context_data()
├── form_valid()
├── get()
└── post()


Important utilities
│
├── filter()
├── get()
├── get_object_or_404()
├── save()
├── redirect()
└── reverse_lazy()


Authentication
│
└── LoginRequiredMixin


URL
│
└── as_view()
```

# 50. Golden Rule

When reading a Django CBV, ask these questions in order:

```text
1. Which CBV?
       ↓
2. Which model?
       ↓
3. Which template?
       ↓
4. Which objects?
       ↓
   get_queryset()
       ↓
5. What extra data?
       ↓
   get_context_data()
       ↓
6. What happens after form submission?
       ↓
   form_valid()
       ↓
7. Where does the user go?
       ↓
   success_url
```

If you understand these **7 questions**, you can understand most basic-to-intermediate Django CBV code.

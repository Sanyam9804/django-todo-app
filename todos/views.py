from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (ListView,CreateView,UpdateView,DeleteView,View,)
from .models import Todo


class TodoListView(LoginRequiredMixin, ListView):

    model = Todo
    template_name = "todos/dashboard.html"
    context_object_name = "todos"
    login_url = reverse_lazy("login")
    paginate_by = 5

    def get_queryset(self):

        queryset = Todo.objects.filter(user=self.request.user)
        status = self.request.GET.get("status")
        priority = self.request.GET.get("priority")

        if status == "pending":
            queryset = queryset.filter(completed=False)

        elif status == "completed":
            queryset = queryset.filter(completed=True)

        if priority in ["low", "medium", "high"]:
            queryset = queryset.filter(priority=priority)

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        all_todos = Todo.objects.filter(user=self.request.user)
        context["total_count"] = all_todos.count()
        context["completed_count"] = all_todos.filter(completed=True).count()
        context["pending_count"] = all_todos.filter(completed=False).count()
        context["current_status"] = self.request.GET.get("status","all")
        context["current_priority"] = self.request.GET.get("priority","all")

        return context


class TodoCreateView(LoginRequiredMixin, CreateView):

    model = Todo
    fields = ["title","description","priority",]
    template_name = "todos/todo_form.html"
    success_url = reverse_lazy("todo_dashboard")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
         # Who created this Todo?
        form.instance.user = self.request.user
        # Now save it normally
        return super().form_valid(form)


class TodoUpdateView(LoginRequiredMixin, UpdateView):

    model = Todo
    fields = ["title","description","priority",]
    template_name = "todos/todo_form.html"
    success_url = reverse_lazy("todo_dashboard")
    login_url = reverse_lazy("login")

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


class TodoDeleteView(LoginRequiredMixin, DeleteView):

    model = Todo
    template_name = "todos/todo_confirm_delete.html"
    success_url = reverse_lazy("todo_dashboard")
    login_url = reverse_lazy("login")

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


class TodoToggleView(LoginRequiredMixin, View):

    login_url = reverse_lazy("login")

    def post(self, request, pk):

        todo = get_object_or_404(Todo,pk=pk,user=request.user)
        todo.completed = not todo.completed
        todo.save()

        return redirect("todo_dashboard")
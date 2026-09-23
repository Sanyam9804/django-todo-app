from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from .forms import SignupForm


class HomeView(TemplateView):
    template_name = "home.html"


class SignupView(FormView):
    template_name = "signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("todo_dashboard")

    def form_valid(self, form):

        user = form.save()
        login(self.request,user)
        return super().form_valid(form)


class UserLoginView(LoginView):
    
    template_name = "login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("todo_dashboard")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")
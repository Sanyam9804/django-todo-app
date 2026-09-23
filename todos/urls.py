from django.urls import path

from .views import (TodoListView,TodoCreateView,TodoUpdateView,TodoDeleteView,TodoToggleView,)


urlpatterns = [

    path("",TodoListView.as_view(),name="todo_dashboard"),
    path("create/",TodoCreateView.as_view(),name="todo_create"),
    path("update/<int:pk>/",TodoUpdateView.as_view(),name="todo_update"),
    path("delete/<int:pk>/",TodoDeleteView.as_view(),name="todo_delete"),
    path("toggle/<int:pk>/",TodoToggleView.as_view(),name="todo_toggle"),
]
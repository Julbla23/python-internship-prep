from django.urls import path
from . import views


urlpatterns = [
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/<int:n>/delete", views.delete_task, name="delete_task"),
]
from django.urls import path
from . import views


urlpatterns = [
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/<int:n>/delete", views.delete_task, name="delete_task"),
    path("tasks/add/", views.add_task, name="add_task"),
    path("tasks/<int:n>/edit/", views.edit_task, name="edit_task"),
    path("tasks/<int:n>/done", views.status_done, name="status_done"),
    path("", views.home, name="home"),
    path("calendar/", views.calendar, name="calendar"),
    path("calendar/<int:year>/<int:month>/<int:day>", views.tasks_by_day, name="tasks_by_day"),
    path("categories/add/", views.add_category, name="add_category"),
]

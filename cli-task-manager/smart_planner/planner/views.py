from datetime import date
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import AddTask
from .models import Task


def task_list(request):
    tasks = Task.objects.filter(planned_date = date.today())
    return render(request, "planner/tasks_list.html", {"tasks": tasks})

"""
Task.object.all() to mój model, czyli tabela w bazie danych <- pobierz wszystkie taski z tabeli Task
objects to manager django do niego się zawsze zwracamy np. Tasks.objects.filter(...)
render() mówi django Weź template HTML, włóż do niego dane i odeślij gotową stronę do przeglądarki.
request - żądnanie użytkownika
planner/tasks)list.html - plik html, który ma zostać pokazany
{"tasks": tasks} - dane przekazane do HTMLa; słownik
views.py:
pobiera dane

template:
wyświetla dane
"""

def delete_task(request, n):
    task = Task.objects.get(id=n)
    task.delete()
    return redirect("task_list")

def status_done(request, n):
    task = Task.objects.get(id=n)
    task.status = "done"
    task.save()
    return redirect("task_list")

def add_task(request):
    if request.method == "POST":
        form = AddTask(request.POST)
        if form.is_valid():
            name = form.cleaned_data['title']
            priority = form.cleaned_data['priority']
            planned_date = form.cleaned_data['planned_date']
            duration_minutes = form.cleaned_data['duration_minutes']
            status = form.cleaned_data['status']
            Task.objects.create(name=name, priority=priority, planned_date=planned_date, duration_minutes=duration_minutes,status=status)
            return redirect("task_list")
    else:
        form = AddTask()
    return render(request, "planner/forms.html", {"form": form})

def home(request):
    return render(request, "planner/home.html")
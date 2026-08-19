from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from jsonschema.validators import validate

from .forms import AddTask, EditTask
from .models import Task, Category
from calendar import monthcalendar, month_name
from datetime import datetime, date, timedelta
import json
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.decorators import login_required


def task_list(request):
    tasks = Task.objects.filter(planned_date__date = date.today()).order_by("position")
    return render(request, "planner/tasks_list.html", {"tasks": tasks})

def change_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        order = data.get("order")
        if order:
            for position, task_id in enumerate(order, 1):
                task = Task.objects.get(id=task_id)
                task.position = position
                task.save()
            return JsonResponse({"success": True})

    return JsonResponse({"success": False})
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


def find_over_lapping_tasks(
        planned_date, duration_minutes, excluded_task_id=None
):
    new_start = planned_date
    new_end = planned_date + timedelta(minutes=duration_minutes)

    tasks = Task.objects.all()

    if excluded_task_id is not None:
        tasks = tasks.exclude(id=excluded_task_id)

    overlapping_tasks = []

    for task in tasks:
        existing_start = task.planned_date
        existing_end = (
            task.planned_date + timedelta(minutes=task.duration_minutes)
        )

        tasks_overlap = (
            new_start < existing_end
            and new_end > existing_start
        )

        if tasks_overlap:
            overlapping_tasks.append(task)

    return overlapping_tasks

def add_task(request):
    if request.method == "POST":
        form = AddTask(request.POST)
        if form.is_valid():
            name = form.cleaned_data['title']
            priority = form.cleaned_data['priority']
            planned_date = form.cleaned_data['planned_date']
            duration_minutes = form.cleaned_data['duration_minutes']
            status = form.cleaned_data['status']
            category= form.cleaned_data['category']

            overlapping_tasks = find_over_lapping_tasks(
                planned_date=planned_date,
                duration_minutes=duration_minutes
            )

            if overlapping_tasks:
                return render(
                    request, "planner/forms.html",
                    {
                        "form" : form,
                        "overlapping_tasks" : overlapping_tasks
                    }
                )
            Task.objects.create(name=name, priority=priority, planned_date=planned_date, duration_minutes=duration_minutes, status=status, category=category)
            return redirect("task_list")
    else:
        form = AddTask()
    return render(request, "planner/forms.html", {"form": form})

def edit_task(request, n):
    task = Task.objects.get(id=n)
    if request.method =="POST":
        form = EditTask(request.POST, instance=task) #bierze dane z formularza, bierze istniejący task, nakłada nowe dane na ten obiekt
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = EditTask(instance=task)
    return render(request, "planner/forms.html", {"form": form,"editing": True})

def home(request):
    return render(request, "planner/home.html")

def calendar(request):
    year = 2026
    month = 8

    calendar_data = monthcalendar(2026,8)

    return render(request, "planner/calendar.html", {
        "calendar_data": calendar_data,
        "month_name": month_name[month],
        "month": month,
        "year": year,
    })

def tasks_by_day(request, year, month, day):
    my_date = date(year, month, day)
    tasks = Task.objects.filter(planned_date__date=my_date)
    return render(request, "planner/tasks_list.html", {"tasks": tasks})

def add_category(request):
    if request.method == "POST":
        category_name = request.POST.get("name").strip()
        if category_name:
            if not Category.objects.filter(name=category_name).exists():
                category = Category.objects.create(
                    name=category_name,
                )
            else:
                raise Exception("Category already exists")
    return redirect("add_task")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'planner/register.html', {'form': form})


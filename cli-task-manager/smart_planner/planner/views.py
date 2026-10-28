from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .forms import AddTask, EditTask
from .models import Task, Category, TaskMoveHistory
from calendar import monthcalendar, month_name
from datetime import datetime, date, timedelta
import json
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate

@login_required
def task_list(request):
    tasks = Task.objects.filter(planned_date__date = date.today(), user=request.user).order_by("position")
    percentage = complete_percentage(request)
    return render(request, "planner/tasks_list.html", {"tasks": tasks, "percentage": percentage})

@login_required
def backlog_tasks_list(request):
    backlog_tasks = Task.objects.filter(planned_date__lt = timezone.now(), status="todo", user=request.user)
    return render(request, "planner/backlog_tasks_list.html", {"backlog_tasks": backlog_tasks})

@login_required
def change_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        order = data.get("order")
        if order:
            for position, task_id in enumerate(order, 1):
                task = get_object_or_404(Task, id=task_id, user=request.user)
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

@login_required
def delete_task(request, n):
    task = get_object_or_404(Task, id=n, user=request.user)
    task.delete()
    return redirect("task_list")

@login_required
def status_done(request, n):
    task = get_object_or_404(Task, id=n, user=request.user)
    task.status = "done"
    task.status_changed_at = timezone.now()
    task.save()
    return redirect("task_list")


def find_over_lapping_tasks(
        user, planned_date, duration_minutes, excluded_task_id=None
):
    new_start = planned_date
    new_end = planned_date + timedelta(minutes=duration_minutes)

    tasks = Task.objects.filter(user=user)

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

@login_required
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
            deadline = form.cleaned_data['deadline']

            overlapping_tasks = find_over_lapping_tasks(
                user=request.user,
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
            Task.objects.create(name=name, priority=priority, planned_date=planned_date, duration_minutes=duration_minutes, status=status, category=category, deadline=deadline, user=request.user)
            return redirect("task_list")
    else:
        form = AddTask()
    return render(request, "planner/forms.html", {"form": form})

@login_required
def edit_task(request, n):
    task = get_object_or_404(Task, id=n, user=request.user)
    old_planned_date = task.planned_date
    if request.method =="POST":
        form = EditTask(request.POST, instance=task) #bierze dane z formularza, bierze istniejący task, nakłada nowe dane na ten obiekt
        if form.is_valid():
            new_planned_date = form.cleaned_data['planned_date']
            if old_planned_date != new_planned_date:
                task.status = "moved"
                task.status_changed_at = timezone.now()
                TaskMoveHistory.objects.create(task=task, old_planned_date=old_planned_date,new_planned_date=new_planned_date)
            form.save()
            return redirect("home")
    else:
        form = EditTask(instance=task)
    return render(request, "planner/forms.html", {"form": form,"editing": True})

@login_required
def home(request):
    return render(request, "planner/home.html",)

@login_required
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

@login_required
def tasks_by_day(request, year, month, day):
    my_date = date(year, month, day)
    tasks = Task.objects.filter(planned_date__date=my_date, user=request.user)
    return render(request, "planner/tasks_list.html", {"tasks": tasks})

@login_required
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

def complete_percentage(request):
    done_tasks = Task.objects.filter(planned_date__date=date.today(), status="done", user=request.user).count()
    all_tasks = Task.objects.filter(planned_date__date=date.today(), user=request.user).count()
    if all_tasks > 0:
        result = 100 * done_tasks / all_tasks
        return f"{result}%"
    else:
        return "0%"


def statistics(user, period_start, period_end):
    today = date.today()
    done_tasks = Task.objects.filter(
        status="done",
        status_changed_at__date__gte=period_start,
        status_changed_at__date__lte=period_end,
        user=user
    ).count()
    moved_tasks = TaskMoveHistory.objects.filter(task__user=user, moved_at__date__gte=period_start, moved_at__date__lte=period_end).count()
    overdue_tasks = Task.objects.filter(status="todo", deadline__lt=today, user=user).count()
    backlog = Task.objects.filter(deadline__isnull=True, status="todo", user=user).count()
    category_stats=Task.objects.filter(
        status="done",
        planned_date__date__gte=period_start,
        planned_date__date__lte=period_end,
        user=user
    ).values("category__name").annotate(count=Count("id"))
    category_stats = list(category_stats)
    for item in category_stats:
        if item["category__name"] is None:
            item["category__name"] = "Bez kategorii"
    done_tasks_by_day = Task.objects.filter(
        status="done",
        status_changed_at__date__gte=period_start,
        status_changed_at__date__lte=period_end,
        user=user
    ).annotate(day=TruncDate("status_changed_at")).values("day").annotate(count=Count("id"))
    done_tasks_by_day = list(done_tasks_by_day)
    return {"done": done_tasks, "moved": moved_tasks, "overdue": overdue_tasks, "backlog": backlog, "category": category_stats, "day_tasks": done_tasks_by_day}

@login_required
def show_weekly_statistics(request):
    today = date.today()
    day_of_week = today.weekday()
    week_start = today - timedelta(days=day_of_week)
    week_end = week_start + timedelta(days=6)
    weekly_statistics = statistics(request.user, week_start, week_end)
    return render(request, "planner/weekly_statistics.html", {"statistics": weekly_statistics})

@login_required
def show_monthly_statistics(request):
    today = date.today()
    month_start = date(today.year, today.month, 1)
    if today.month == 12:
        next_month_start = date(today.year + 1, 1,1)
    else:
        next_month_start = date(today.year, today.month + 1, 1)
    month_end = next_month_start - timedelta(days=1)
    monthly_statistics = statistics(request.user, month_start, month_end)
    return render(request, "planner/monthly_statistics.html", {"statistics": monthly_statistics})

@login_required
def show_quarterly_statistics(request):
    today = date.today()
    quarter_start_month = ((today.month - 1) // 3) * 3 + 1
    quarter_start = date(today.year, quarter_start_month, 1)
    next_quarter_start_month = quarter_start_month + 3
    if next_quarter_start_month > 12:
        next_quarter_start = date(today.year + 1, 1,1)
    else:
        next_quarter_start = date(today.year, next_quarter_start_month, 1)
    quarter_end = next_quarter_start - timedelta(days=1)
    quarterly_statistics = statistics(request.user, quarter_start, quarter_end)
    return render(request, "planner/quarterly_statistics.html", {"statistics": quarterly_statistics})



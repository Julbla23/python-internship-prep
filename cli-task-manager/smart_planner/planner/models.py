from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

STATUS_CHOICES = [
    ("todo", "Do zrobienia"),
    ("done", "Zrobione"),
    ("moved", "Przesunięte"),
    ("cancelled", "Wykreślone")
]

PRIORITY_CHOICES = [
    ("low", "Można prokrastynować"),
    ("medium", "Lepiej to zrób"),
    ("high", "Musisz to zrobić")
]

class Task(models.Model):
    name = models.CharField(max_length=100)
    planned_date = models.DateField()
    deadline = models.DateField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="low")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    user = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null = True,
        blank = True,
    )

    def __str__(self):
        return f"{self.name} ({self.duration_minutes}) due {self.deadline} ({self.priority})"

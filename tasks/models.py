from django.db import models
from django.utils import timezone

# 1. BaseModel with created_at and updated_at
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# 2. Priority
class Priority(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priorities"

    def __str__(self):
        return self.name


# 3. Category
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# 4. Task
class Task(BaseModel):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    deadline = models.DateTimeField()
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# 5. SubTask
class SubTask(BaseModel):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    title = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def parent_task_name(self):
        return self.task.title


# 6. Note
class Note(BaseModel):
    task = models.ForeignKey(Task, related_name='notes', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Note for {self.task.title}"
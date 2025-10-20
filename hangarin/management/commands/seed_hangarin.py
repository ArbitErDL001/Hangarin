from django.core.management.base import BaseCommand
from django.utils import timezone
from hangarin.models import Category, Priority, Task, SubTask, Note, STATUS_CHOICES
from faker import Faker
import random

class Command(BaseCommand):
    help = "Seed the database with demo Categories, Priorities, Tasks, SubTasks, and Notes."

    def add_arguments(self, parser):
        parser.add_argument('--tasks', type=int, default=30, help='How many tasks to create')
        parser.add_argument('--subtasks-per-task', type=int, default=2, help='How many subtasks per task')
        parser.add_argument('--notes-per-task', type=int, default=2, help='How many notes per task')

    def handle(self, *args, **options):
        fake = Faker()

       
        priority_names = ["high", "medium", "low", "critical", "optional"]
        category_names = ["Work", "School", "Personal", "Finance", "Projects"]

       
        priorities = []
        for name in priority_names:
            p, _ = Priority.objects.get_or_create(name=name.capitalize())
            priorities.append(p)

       
        categories = []
        for name in category_names:
            c, _ = Category.objects.get_or_create(name=name)
            categories.append(c)

        status_values = [s[0] for s in STATUS_CHOICES]  

        task_count = options['tasks']
        subtasks_per_task = options['subtasks_per_task']
        notes_per_task = options['notes_per_task']

        for _ in range(task_count):
            title = fake.sentence(nb_words=5)  
            description = fake.paragraph(nb_sentences=3) 
            status = fake.random_element(elements=status_values) 

           
            naive_dt = fake.date_time_this_month()
            deadline = timezone.make_aware(naive_dt)

            task = Task.objects.create(
                title=title,
                description=description,
                status=status,
                deadline=deadline,
                priority=random.choice(priorities),
                category=random.choice(categories),
            )

            for _ in range(subtasks_per_task):
                SubTask.objects.create(
                    task=task,
                    title=fake.sentence(nb_words=5),
                    status=fake.random_element(elements=status_values),
                )

            for _ in range(notes_per_task):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=3),
                )

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {task_count} tasks, {subtasks_per_task} subtasks/task, {notes_per_task} notes/task."
        ))

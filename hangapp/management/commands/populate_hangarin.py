from django.core.management.base import BaseCommand
from django.utils import timezone
from hangapp.models import Category, Priority, Task, SubTask, Note
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Populates the Hangarin database with sample data as per specification'

    def handle(self, *args, **options):
        # Clear existing data
        SubTask.objects.all().delete()
        Note.objects.all().delete()
        Task.objects.all().delete()
        Category.objects.all().delete()
        Priority.objects.all().delete()

        # Manually add Priority and Category
        priority_names = ['High', 'Medium', 'Low', 'Critical', 'Optional']
        category_names = ['Work', 'School', 'Personal', 'Finance', 'Projects']

        priorities = [Priority.objects.create(name=name) for name in priority_names]
        categories = [Category.objects.create(name=name) for name in category_names]

        # Generate 20 Tasks
        tasks = []
        for _ in range(20):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5).rstrip('.'),
                description=fake.paragraph(nb_sentences=3),
                status=fake.random_element(elements=("Pending", "In Progress", "Completed")),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                priority=random.choice(priorities),
                category=random.choice(categories)
            )
            tasks.append(task)

        # SubTasks for first 10 tasks
        for task in tasks[:10]:
            for _ in range(random.randint(1, 3)):
                SubTask.objects.create(
                    title=fake.sentence(nb_words=4).rstrip('.'),
                    status=fake.random_element(elements=("Pending", "In Progress", "Completed")),
                    task=task
                )

        # Notes for first 15 tasks
        for task in tasks[:15]:
            Note.objects.create(
                task=task,
                content=fake.paragraph(nb_sentences=2)
            )

        self.stdout.write(
            self.style.SUCCESS('🎉 Successfully populated Hangarin database!')
        )
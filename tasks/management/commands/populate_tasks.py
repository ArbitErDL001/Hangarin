from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from tasks.models import Task, SubTask, Note, Priority, Category
import random

class Command(BaseCommand):
    help = 'Populate database with fake tasks, subtasks, and notes'

    def handle(self, *args, **kwargs):
        fake = Faker()
        priorities = list(Priority.objects.all())
        categories = list(Category.objects.all())

        if not priorities or not categories:
            self.stdout.write(self.style.ERROR("❌ Priority or Category is empty. Add them first!"))
            return

        for _ in range(20):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5).rstrip('.'),
                description=fake.paragraph(nb_sentences=3),
                status=fake.random_element(elements=("Pending", "In Progress", "Completed")),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                priority=random.choice(priorities),
                category=random.choice(categories)
            )

            # Create 1–3 subtasks
            for _ in range(random.randint(1, 3)):
                SubTask.objects.create(
                    title=fake.sentence(nb_words=4).rstrip('.'),
                    status=fake.random_element(elements=("Pending", "In Progress", "Completed")),
                    task=task
                )

            # Create 0–2 notes
            for _ in range(random.randint(0, 2)):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=2)
                )

        self.stdout.write(self.style.SUCCESS('✅ Successfully populated 20 tasks with subtasks and notes!'))
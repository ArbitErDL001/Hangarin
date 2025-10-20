from django.test import TestCase
from django.urls import reverse
from .models import Category, Priority, Task, SubTask, Note
from django.utils import timezone


class CRUDViewsSmokeTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Work")
        self.priority = Priority.objects.create(name="High")
        self.task = Task.objects.create(
            title="Initial Task",
            description="Test desc",
            status="Pending",
            deadline=timezone.now(),
            priority=self.priority,
            category=self.category,
        )

    def test_category_list_and_create(self):
        # List
        resp = self.client.get(reverse('category-list'))
        self.assertEqual(resp.status_code, 200)
        # Create
        resp = self.client.post(reverse('category-add'), {"name": "Personal"}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Category.objects.filter(name="Personal").exists())

    def test_priority_list_and_create(self):
        resp = self.client.get(reverse('priority-list'))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(reverse('priority-add'), {"name": "Low"}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Priority.objects.filter(name="Low").exists())

    def test_task_list_and_create(self):
        resp = self.client.get(reverse('task-list'))
        self.assertEqual(resp.status_code, 200)
        payload = {
            "title": "New Task",
            "description": "Something",
            "status": "Pending",
            "deadline": (timezone.now() + timezone.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
            "priority": self.priority.id,
            "category": self.category.id,
        }
        resp = self.client.post(reverse('task-add'), payload, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Task.objects.filter(title="New Task").exists())

    def test_subtask_list_and_create(self):
        resp = self.client.get(reverse('subtask-list'))
        self.assertEqual(resp.status_code, 200)
        payload = {
            "task": self.task.id,
            "title": "Sub 1",
            "status": "Pending",
        }
        resp = self.client.post(reverse('subtask-add'), payload, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(SubTask.objects.filter(title="Sub 1").exists())

    def test_note_list_and_create(self):
        resp = self.client.get(reverse('note-list'))
        self.assertEqual(resp.status_code, 200)
        payload = {
            "task": self.task.id,
            "content": "Remember to test",
        }
        resp = self.client.post(reverse('note-add'), payload, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Note.objects.filter(content__icontains="Remember").exists())

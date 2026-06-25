from django.test import TestCase, Client
from django.utils import timezone
from datetime import datetime
from todo.models import Task


# クラスの前には2行空ける
class SampleTestCase(TestCase):
    def test_sample1(self):
        self.assertEqual(1 + 2, 3)


class TaskModelTestCase(TestCase):
    def test_create_task(self):
        due = timezone.make_aware(datetime(2024, 6, 30, 23, 59, 59))
        task = Task(title='task1', due_at=due)
        task.save()
        task = Task.objects.get(pk=task.pk)
        self.assertEqual(task.title, 'task1')
        self.assertFalse(task.completed)
        self.assertEqual(task.due_at, due)

    def test_create_task2(self):
        task = Task(title='task2')
        task.save()
        task = Task.objects.get(pk=task.pk)
        self.assertEqual(task.title, 'task2')
        self.assertFalse(task.completed)
        self.assertIsNone(task.due_at)

    def test_is_overdue_past(self):
        due = timezone.make_aware(datetime(2024, 6, 30, 23, 59, 59))
        current = timezone.make_aware(datetime(2024, 7, 1, 0, 0, 0))
        task = Task(title='task1', due_at=due)
        task.save()
        self.assertTrue(task.is_overdue(current))
    
    def test_detail_get_success(self):
        task = Task(title='task1', due_at=timezone.make_aware(datetime(2024, 7, 1)))
        task.save()
        client = Client()
        response = client.get('/{}/'.format(task.pk))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response.template[0].name, 'todo/detail.html')
        self.assertContains(response.context['task'], task)
    
    def test_detail_get_fail(self):
        client = Client()
        response = client.get('/1/')

        self.assertEqual(response.status_code, 404)

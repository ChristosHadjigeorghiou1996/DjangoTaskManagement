from django.db import IntegrityError
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate
from .models import User, Comment, Label, Task

from datetime import date
from .helpers.CalendarHelper import CalendarHelper
# Create your tests here.

class UserModelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testUser", password="testPassword")
    
    def test_user_credentials(self) -> None:
        self.assertEqual(self.user.username, "testUser")
        self.assertTrue(self.user.check_password("testPassword"))

    def test_invalid_credentials(self) -> None:
        invalid_user = authenticate(username="testUser", password="invalid")
        self.assertIsNone(invalid_user)

    def test_no_password_credentials(self) -> None:
        invalid_user = authenticate(username="testUser")
        self.assertIsNone(invalid_user)

class TaskModelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testUser", password="testPassword")
        self.user2 = User.objects.create_user(username="testUser2", password="testPassword2")
        self.task = Task.objects.create(
            title = "Task",
            description = "Test task",
            created_by = self.user,
            due_date = "2023-10-28"
        )

        self.label = Label.objects.create(name='Test Label')
        self.task.labels.add(self.label)
        self.task.shared_with.add(self.user2)

    def test_task_creation(self) -> None:
        self.assertEqual(self.task.title, "Task")
        self.assertEqual(self.task.description, "Test task")
        self.assertEqual(self.task.created_by, self.user)
    
    # Integrity error due to not having foreign key
    def test_invalid_task_creation_integrity_error(self) -> None:
        with self.assertRaises(IntegrityError):
            invalid_task = Task.objects.create(
                title = "Task"
            )

    def test_shared_with_field(self):
        self.assertEqual(list(self.task.shared_with.all()), [self.user2])

    def test_created_by_field(self):
        self.assertEqual(self.task.created_by, self.user)


class LabelModelTestCase(TestCase):
    def setUp(self) -> None:
        self.label = Label.objects.create(name="deadline_1")

    def test_label_creation(self) -> None:
        self.assertEqual(self.label.name, "deadline_1")

class CommentModelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testUser", password="testPassword")
        self.task = Task.objects.create(
            title = "Task",
            description = "Test task",
            created_by = self.user,
            due_date = "2023-10-28"
        )
        self.comment = Comment.objects.create(
            task=self.task,
            author=self.user,
            body="Dummy comment",
        )

    def test_comment_creation(self) -> None:
        self.assertEqual(self.comment.task, self.task)
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.body, "Dummy comment")

    def test_invalid_comment_integrity_error(self) -> None:
        with self.assertRaises(IntegrityError):
            comment = Comment.objects.create(
                task=self.task,
            )

    def test_invalid_comment_no_body_integrity_error(self) -> None:
        with self.assertRaises(IntegrityError):
            comment = Comment.objects.create(
                task=self.task,
                author=self.user,
                body=None
            )


class CalendarHelperTestCase(TestCase):

    def test_get_last_day_of_month(self):
        # January 2023
        self.assertEqual(CalendarHelper.get_last_day_of_month(2023, 1), date(2023, 1, 31))
        # February 2023 (non-leap year)
        self.assertEqual(CalendarHelper.get_last_day_of_month(2023, 2), date(2023, 2, 28))
        # February 2024 (leap year)
        self.assertEqual(CalendarHelper.get_last_day_of_month(2024, 2), date(2024, 2, 29))
        # November 2023
        self.assertEqual(CalendarHelper.get_last_day_of_month(2023, 11), date(2023, 11, 30))

    def test_get_next_month(self):
        # February 28, 2023
        self.assertEqual(CalendarHelper.get_next_month(date(2023, 2, 28)), "2023-03-01")
        # November 30, 2022
        self.assertEqual(CalendarHelper.get_next_month(date(2022, 11, 30)), "2022-12-01")
        # December 31, 2023
        self.assertEqual(CalendarHelper.get_next_month(date(2023, 12, 31)), "2024-01-01")

    def test_get_previous_month(self):
        # February 28, 2023
        self.assertEqual(CalendarHelper.get_previous_month(date(2023, 2, 28)), "2023-01-01")
        # November 30, 2022
        self.assertEqual(CalendarHelper.get_previous_month(date(2022, 11, 30)), "2022-10-01")
        # January 1, 2023
        self.assertEqual(CalendarHelper.get_previous_month(date(2023, 1, 1)), "2022-12-01")

    def test_get_next_month_leap_year(self):
        # February 29, 2024 (leap year)
        self.assertEqual(CalendarHelper.get_next_month(date(2024, 2, 29)), "2024-03-01")

    def test_get_previous_month_leap_year(self):
        # February 29, 2024 (leap year)
        self.assertEqual(CalendarHelper.get_previous_month(date(2024, 2, 29)), "2024-01-01")

    def test_populate_calendar_days_for_month(self):
        # January 2023
        january_2023 = date(2023, 1, 1)
        expected_days_january_2023 = [
            date(2023, 1, x) for x in range(1, 31+1)
        ]
        self.assertEqual(CalendarHelper.populate_calendar_days_for_month(january_2023), expected_days_january_2023)

        # February 2024 (leap year)
        february_2024 = date(2024, 2, 1)
        expected_days_february_2024 = [
            date(2024, 2, x) for x in range(1, 29+1)
        ]
    
        self.assertEqual(CalendarHelper.populate_calendar_days_for_month(february_2024), expected_days_february_2024)

        # November 2023
        november_2023 = date(2023, 11, 1)
        expected_days_november_2023 = [
            date(2023, 11, x) for x in range(1, 30+1)
        ]
        self.assertEqual(CalendarHelper.populate_calendar_days_for_month(november_2023), expected_days_november_2023)


class ProfileViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

    def test_profile_view_with_valid_user_id(self):
        response = self.client.get(reverse('user-profile', args=[str(self.user.id)]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user_profile'], self.user)

    def test_profile_view_with_invalid_user_id(self):
        response = self.client.get(reverse('user-profile', args=['999999999']))
        self.assertEqual(response.status_code, 404)

    def test_profile_view_for_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('user-profile', args=[str(self.user.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user_profile'], self.user)

    def test_profile_view_for_unauthenticated_user(self):
        response = self.client.get(reverse('user-profile', args=[str(self.user.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user_profile'], self.user)

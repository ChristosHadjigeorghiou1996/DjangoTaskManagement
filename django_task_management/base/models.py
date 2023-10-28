from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    """
    Basic User class including a bio and 
        profile pic option
    """
    name = models.CharField(max_length=200, null=True)
    bio = models.TextField(null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class Label(models.Model):
    """
    Label to filter tasks on and show number of
        tasks in each label
    """
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Task(models.Model):
    """
    Task model that allows user to create task
        including the status, label and if it is shared
    """
    STATUS_CHOICES = (
        ('Not Started', 'Not Started'),
        ('Started', 'Started'),
        ('Completed', 'Completed'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Started')
    labels = models.ManyToManyField(Label, related_name='tasks', blank=True)
    image_attachment = models.ImageField(upload_to='task_images/', null=True, blank=True)
    assigned_to = models.ManyToManyField(User, related_name='assigned_tasks', blank=True)
    is_shared = models.BooleanField(default=False)

    class Meta:
        """
        Order the Tasks according to which was the most recent
        """
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class SharedTask(models.Model):
    """
    Model to share task with different users
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    patricipants = models.ManyToManyField(User, related_name="participants", blank=True )
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_tasks')
    shared_with = models.ManyToManyField(User, related_name='tasks_shared_with')
    shared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} shared by {self.shared_by.username}"

class Comment(models.Model):
    """
    Model to write comments to tasks and including
        images
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image_attachment = models.ImageField(upload_to='comment_images/', null=True, blank=True)

    class Meta:
        """
        Order the Comment according to which was the most recent
        """
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.task.title}"


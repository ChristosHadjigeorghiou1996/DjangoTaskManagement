from django.contrib import admin
from .models import User, Task, Comment, Label
# Register your models here.
admin.site.register(User)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Label)
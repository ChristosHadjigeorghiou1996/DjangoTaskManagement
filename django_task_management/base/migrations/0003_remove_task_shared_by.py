# Generated by Django 4.2.6 on 2023-11-16 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_task_shared_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='shared_by',
        ),
    ]

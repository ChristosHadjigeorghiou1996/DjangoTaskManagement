# Generated by Django 4.2.6 on 2023-11-11 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_remove_sharedtask_shared_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('NotStarted', 'NotStarted'), ('Started', 'Started'), ('Completed', 'Completed')], default='NotStarted', max_length=20),
        ),
    ]
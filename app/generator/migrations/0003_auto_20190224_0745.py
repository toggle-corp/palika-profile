# Generated by Django 2.1.3 on 2019-02-24 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0002_auto_20190221_1127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generator',
            name='task',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]

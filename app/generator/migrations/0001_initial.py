# Generated by Django 2.1.3 on 2019-02-21 11:25

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Export',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=255, upload_to='exports/')),
            ],
        ),
        migrations.CreateModel(
            name='Generator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=255, upload_to='documents/')),
                ('errors', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('success', 'Success'), ('failure', 'Failure')], default='pending', max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='generator',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='generator.Task'),
        ),
        migrations.AddField(
            model_name='export',
            name='generator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generator.Generator'),
        ),
    ]

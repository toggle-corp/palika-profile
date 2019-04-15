# Generated by Django 2.1.7 on 2019-03-12 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0008_export_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generator',
            name='status',
            field=models.CharField(choices=[('not_processed', 'Not Processed'), ('pending', 'Pending'), ('success', 'Success'), ('failure', 'Failure')], default='not_processed', max_length=30),
        ),
    ]
# Generated by Django 3.0.11 on 2020-11-08 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_validated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='validated',
        ),
        migrations.AddField(
            model_name='user',
            name='is_validated',
            field=models.BooleanField(default=False, verbose_name='Has the User been Validated?'),
        ),
    ]

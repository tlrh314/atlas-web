# Generated by Django 3.0.11 on 2020-11-14 13:27

import atlas_web.users.managers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email Address')),
                ('first_name', models.CharField(max_length=42, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=42, verbose_name='Last Name')),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='Active')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='Staff')),
                ('is_validated', models.BooleanField(default=False, verbose_name='Has the User been Validated?')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date Last Changed')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='has_changed_accounts', to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', atlas_web.users.managers.UserManager()),
            ],
        ),
    ]

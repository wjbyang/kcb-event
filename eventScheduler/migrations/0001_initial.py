# Generated by Django 5.0.1 on 2024-02-07 20:35

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.TextField()),
                ('location', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('image', models.TextField(blank=True, null=True)),
                ('start_time', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('image', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupToEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hosting', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eventScheduler.event')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eventScheduler.group')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('image', models.TextField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('isAdmin', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='eventScheduler.organization')),
            ],
        ),
        migrations.CreateModel(
            name='UserToEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attending', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eventScheduler.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='eventScheduler.user')),
            ],
        ),
    ]

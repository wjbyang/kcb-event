# Generated by Django 5.0.1 on 2024-01-30 22:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventScheduler', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='startTime',
            new_name='start_time',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='firstName',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='lastName',
            new_name='last_name',
        ),
        migrations.AddField(
            model_name='user',
            name='isAdmin',
            field=models.BooleanField(default=False),
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
    ]

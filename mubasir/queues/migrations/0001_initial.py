# Generated by Django 2.2.13 on 2020-09-30 12:32

import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import hipo_django_core.models
import hipo_django_core.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('slack', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.BigIntegerField(default=hipo_django_core.utils.generate_unique_id, editable=False, primary_key=True, serialize=False)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('update_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=32, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')])),
                ('items', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created_by', models.CharField(max_length=155)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='queues', to='slack.SlackChannel')),
            ],
            options={
                'abstract': False,
            },
            bases=(hipo_django_core.models.LogEntryMixin, models.Model),
        ),
    ]
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.validators import RegexValidator

from hipo_django_core.models import AbstractBaseModel

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class Queue(AbstractBaseModel):
    name = models.CharField(max_length=32, validators=[alphanumeric])
    items = JSONField()

    channel = models.ForeignKey("slack.SlackChannel", related_name="queues", on_delete=models.CASCADE)

    created_by = models.CharField(max_length=155)

    def __str__(self):
        return f"{self.name}"

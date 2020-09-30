from django.db import models
from django.contrib.postgres.fields import JSONField

from hipo_django_core.models import AbstractBaseModel


class Queue(AbstractBaseModel):
    name = models.CharField()
    items = JSONField()
    channel = models.ForeignKey("slack.SlackChannel", related_name="queues", on_delete=models.CASCADE)

    created_by = models.CharField()

    def __str__(self):
        return f"{self.name}"

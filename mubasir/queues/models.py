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


class SlackWorkspace(models.Model):
    access_token = models.CharField(max_length=255)
    team_name = models.CharField(max_length=255)
    team_id = models.CharField(max_length=255, unique=True)
    team_domain = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Slack Workspace"
        verbose_name_plural = "Slack Workspaces"

    def __str__(self):
        return f"{self.team_name}"

    def update_team_info(self):
        """
        Update team information
        """
        client = slack.WebClient(token=self.access_token)

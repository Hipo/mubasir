from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.validators import RegexValidator

from hipo_django_core.models import AbstractBaseModel

alphanumeric_validator = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class Queue(AbstractBaseModel):
    name = models.CharField(max_length=32, validators=[alphanumeric_validator])
    items = JSONField()

    channel = models.ForeignKey("slack.SlackChannel", related_name="queues", on_delete=models.CASCADE)

    created_by = models.CharField(max_length=155)

    def __str__(self):
        return f"{self.name}"

    def get_queue_members_names_in_order(self):
        return [member["name"] for member in self.items]

    def get_items_as_markdown_attachment(self):
        member_names = self.get_queue_members_names_in_order()
        member_names[0] = '• ' + member_names[0] + ' (Next)'
        return [
            {
                "color": "#32a852",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{self.name} Queue:*"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": '\n • '.join(member_names)
                        }
                    }
                ]
            }
        ]

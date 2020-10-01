from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from mubasir.slack.models import SlackWorkspace, SlackChannel
from mubasir.queues.models import Queue

import json
import pprint
import requests
from mubasir.users.models import User

SLACK_OAUTH_URL = "https://slack.com/api/oauth.access"
SLACK_OAUTH_SCOPES = "channels:read,chat:write:bot,commands,files:write:user,team:read,users:read"

SLACK_COMMAND_CREATE = 'create'
SLACK_COMMAND_DEQUEUE = 'dequeue'
SLACK_COMMAND_ENQUEUE = 'enqueue'
SLACK_COMMAND_INFO = 'info'
SLACK_COMMAND_QUEUES = 'queues'

ALLOWED_COMMANDS = [
    SLACK_COMMAND_CREATE,
    SLACK_COMMAND_DEQUEUE,
    SLACK_COMMAND_ENQUEUE,
    SLACK_COMMAND_INFO,
    SLACK_COMMAND_QUEUES
]


class SlackOAuthView(View):
    """
    Authenticates the workspace, saves or updates internal list of channels
    """
    def get(self, request):
        auth_code = request.GET.get('code')

        if not auth_code:
            return render(request, 'slack/authenticate.html', {
                'client_id': settings.SLACK_CLIENT_ID,
                'oauth_scope': SLACK_OAUTH_SCOPES,
            })

        response = requests.get(SLACK_OAUTH_URL, params={
            'client_id': settings.SLACK_CLIENT_ID,
            'client_secret': settings.SLACK_CLIENT_SECRET,
            'code': auth_code,
        }).json()

        access_token = response.get('access_token')
        team_name = response.get('team_name')
        team_id = response.get('team_id')
        
        if not access_token or not team_id:
            return render(request, 'slack/authenticate.html', {
                'client_id': settings.SLACK_CLIENT_ID,
                'oauth_scope': SLACK_OAUTH_SCOPES,
            })
        
        workspace, created = SlackWorkspace.objects.update_or_create(
            team_id=team_id,
            defaults={
                'access_token': access_token,
                'team_name': team_name,
            }
        )
        
        workspace.update_channels()
        workspace.update_team_info()
        
        return render(request, 'slack/success.html')


@method_decorator(csrf_exempt, name='dispatch')
class SlackCommandView(View):
    """
    Handles incoming commands from Slack
    """
    def post(self, request):
        text_list = request.POST.get('text').split()
        team_id = request.POST.get('team_id')
        user_id = request.POST.get('user_id')
        channel_id = request.POST.get('channel_id')

        if not text_list:
            return JsonResponse({
                'response_type': 'ephemeral',
                'text': "You should specify a command to run mubasir. "
                        "Please try one of the allowed commands. You can type (/mubasir info) to see details."
            })

        command = text_list[0]
        arguments = text_list[1:]

        if command not in ALLOWED_COMMANDS:
            return JsonResponse({
                'response_type': 'ephemeral',
                'text': "Sorry, I don't know this command. Please try one of the allowed commands."
            })

        try:
            workspace = SlackWorkspace.objects.get(team_id=team_id)
        except:
            return JsonResponse({
                'response_type': 'ephemeral',
                'text': "Your workspace doesn't seem to be setup, please install mubasir first."
            })

        try:
            channel = SlackChannel.objects.get(channel_id=channel_id)
        except:
            workspace.update_channels()
            channel = SlackChannel.objects.get(channel_id=channel_id)

        members = channel.get_all_channel_members()
        message = None
        attachments = []

        if command == SLACK_COMMAND_CREATE:
            if not arguments:
                return JsonResponse({
                    'response_type': 'ephemeral',
                    'text': "You should specify a name for queue. (/mubasir create <queue_name>)"
                })

            queue, created = Queue.objects.get_or_create(
                name=arguments[0],
                channel_id=channel.id,
                channel__workspace__team_id=team_id,
                defaults={
                    "items": members,
                    "created_by": user_id
                }
            )

            if not created:
                return JsonResponse({
                    'response_type': 'ephemeral',
                    'text': "There is a queue with this name in this channel, please try another name."
                })

            message = f"The queue *{arguments[0]}* is created successfully.\n"
            attachments = queue.get_items_as_markdown_attachment()

        elif command == SLACK_COMMAND_ENQUEUE:

            try:
                queue = Queue.objects.get(
                    name=arguments[0],
                    channel_id=channel.id,
                    channel__workspace__team_id=team_id
                )
            except:
                return JsonResponse({
                    'response_type': 'ephemeral',
                    'text': "There is no such a queue with this name in this channel."
                })

            if arguments[1] not in [item["name"] for item in queue.items]:
                queue.items.append({"name": arguments[1]})
                queue.save()
            else:
                return JsonResponse({
                    'response_type': 'ephemeral',
                    'text': "This member is already in the queue."
                })

            message = f"*{arguments[1]}* is added into queue *{arguments[0]}* successfully.\n"
            attachments = queue.get_items_as_markdown_attachment()

        elif command == SLACK_COMMAND_DEQUEUE:

            try:
                queue = Queue.objects.get(
                    name=arguments[0],
                    channel_id=channel.id,
                    channel__workspace__team_id=team_id
                )
            except:
                return JsonResponse({
                    'response_type': 'ephemeral',
                    'text': "There is no such a queue with this name in this channel."
                })

            next_member = queue.items.pop(0)
            queue.save()

            message = f"Next member *{next_member['name']}* popped from queue *{arguments[0]}* successfully.\n"
            attachments = queue.get_items_as_markdown_attachment()

        elif command == SLACK_COMMAND_INFO:
            message = "List of commands:"
            attachments = [
                {"text": "- */mubasir create <queue_name>* (Creates a queue that includes all members of the channel.) \n"},
                {"text": "- */mubasir dequeue <queue_name>* (Pops out the next member of the queue and shows its name.) \n"},
                {"text": "- */mubasir enqueue <queue_name>* <member_name> (Appends given member to the queue.) \n"},
                {"text": "- */mubasir queues* (Shows all of the channel queues.) \n"}
            ]

        if message:
            return JsonResponse({
                'text': message,
                "attachments": attachments
            })
        else:
            return HttpResponse(status=200)

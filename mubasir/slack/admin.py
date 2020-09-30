from django.contrib import admin

from mubasir.slack.models import SlackWorkspace, SlackChannel


class SlackWorkspaceAdmin(admin.ModelAdmin):
    pass


class SlackChannelAdmin(admin.ModelAdmin):
    pass


admin.site.register(SlackWorkspace, SlackWorkspaceAdmin)
admin.site.register(SlackChannel, SlackChannelAdmin)

from django.contrib import admin
from django.urls import path

from django.conf.urls import url
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include(('mubasir.core.urls', 'core'), namespace='core')),
    url(r'^slack/', include(('mubasir.slack.urls', 'slack'), namespace='slack')),
]

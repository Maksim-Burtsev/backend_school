from django.contrib import admin
from django.urls import path, include

from main.api import api

import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api.urls),
    path('__debug__/', include(debug_toolbar.urls)),
]

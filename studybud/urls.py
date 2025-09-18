# Utilize the following imports
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),        #  URL for the admin page
    path('', include('base.urls')),         #  URLs from the BASE app
    path('api/', include('base.api.urls'))  #  URLS from the app's API
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
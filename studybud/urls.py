# Utilize the following imports
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),    #  URL for the admin page
    path('', include('base.urls'))      #  URLs from the BASE app
]


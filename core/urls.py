from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Route any /api/v1/ traffic to our storage app
    path('api/v1/', include('storage.urls')), 
]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('app.urls')),
    #Rest framework urls 
    path('api/', include('app.api.urls')),
    path('api/auth/', include('authentication.urls')),
    
]

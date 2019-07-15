"""bifcoin URL Configuration
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('blockchain.urls')),
    path('user/', include('user.urls')),
    path('blockchain/', include('blockchain.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

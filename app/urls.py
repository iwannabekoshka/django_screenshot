from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
]

urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)
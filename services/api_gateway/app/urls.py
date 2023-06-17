
from django.urls import path, include

urlpatterns = [
    path('', include('apigateway.urls')),
]

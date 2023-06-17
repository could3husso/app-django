from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from articles import views

urlpatterns = [
    path('articles/', views.articles),
    path('articles/<str:pk>/', views.ArticleDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
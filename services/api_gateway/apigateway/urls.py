from django.urls import path

from apigateway import views

app_name = 'apigateway'

urlpatterns = [

    path('posts', views.posts, name='articles_service'),
    path('comments', views.comments, name='comments_service'),

    # path('post/<str:post_id>/', views.post_detail, name='post'),
    # path('post/<str:post_id>/delete/', views.delete_post, name='delete_post'),
    # path('post/<str:post_id>/update/', views.update_post, name='update_post'),
    
    # path('comment/post/<str:post_id>/', views.add_comment, name='add_comment'),
    # path('comment/<str:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    # path('comment/<str:comment_id>/update/', views.update_comment, name='update_comment'),
]
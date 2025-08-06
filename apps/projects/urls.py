from django.urls import path
from . import views  # Import views from the current app

urlpatterns = [
    path('', views.home, name='blog-home'),
    # path('', views.post_list, name='post_list'),  # Handles 'blog/'
    # path('<int:post_id>/', views.post_detail, name='post_detail'),  # Handles 'blog/1/'
    # path('category/<str:category>/', views.posts_by_category, name='posts_by_category'),
]
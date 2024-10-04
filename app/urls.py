from django.urls import path
from .views import *
urlpatterns = [
    path('',index,name='index'),
    path('blog_details/<int:blog_id>/',blog_details,name='blog_details'),
    path('login_view',login_view,name='login_view'),
    path('register',register,name='register'),
    path('logout_view',logout_view,name='logout_view'),
    path('add_post',add_post,name='add_post'),
    path('dashboard',dashboard,name='dashboard'),
    path('edit_blog/<int:blog_id>/',edit_blog,name='edit_blog'),
    path('delete_blog/<int:blog_id>/',delete_blog,name='delete_blog'),
    
    path('edit_news/<int:news_id>/',edit_news,name='edit_news'),
    path('news_details/<int:news_id>/',news_details,name='news_details'),
    path('add_news',add_news,name='add_news'),
    path('delete_news/<int:news_id>/',delete_news,name='delete_news'),
    path('user_profile/<int:user_profile_id>/',user_profile,name='user_profile'),
    path('edit_profile/',edit_profile,name='edit_profile'),
    path('filter_view/',filter_view,name ='filter_view'),
    path('search_result/',search_result,name ='search_result'),
]
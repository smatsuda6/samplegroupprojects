from django.conf.urls import include, url
from django.urls import path, re_path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='posts', permanent=False)),#views.show_home_page, name='home'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('logout/', views.logout, name='logout'),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('redirect_new_users/', views.redirect_new_users, name='redirect_new_users'),
    path('new_user_settings/', views.new_user_settings, name='new_user_settings'),
    path('new_user_skills/', views.new_user_skills, name='new_user_skills'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('posts/comment_delete/<int:pk>', views.comment_delete, name='comment_delete'),
    path('posts/sort_by_newest', views.sort_by_newest, name='sort_by_newest'),
    path('posts/sort_by_oldest', views.sort_by_oldest, name='sort_by_oldest'),
    path('posts/sort_by_top', views.sort_by_top, name='sort_by_top'),
    path('posts/sort_by_bottom', views.sort_by_bottom, name='sort_by_bottom'),
    path('notifications/', views.notifications, name='notifications'),
    path('settings/', views.user_settings, name='user_settings'),
    path('skills/', views.edit_skills, name='edit_skills'),
    path('profile/<username>/', views.profile, name='profile'),
    path('profile/<username>/upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path('posts/new/', views.post_new, name='post_new'),
    path('posts/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('posts/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:pk>/like/', views.like_post, name='like_post'),
    url(r'^search/', views.search, name="search"),
    url(r'^like_post/$', views.like_post, name='like_post'),
    url(r'^connect_with_profile/$', views.connect_with_profile, name='connect_with_profile'),
    re_path(r'posts/(?P<author>[\w.@+-]+)/(?P<id>\d+)/', views.post_detail_view, name='post_detail'),
]

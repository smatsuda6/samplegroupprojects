from django.conf.urls import url, include
from django.urls import path
from . import views

urlpatterns = [
    #path('auth/', include('social_django.urls', namespace='social')),
    path('login/', views.login, name='login'),
    # path('signup/', views.sign_up, name='signup'),
    #path('logout/', views.logout, name='logout'),
    path('searchbar/', views.search_nav, name="searchbar"),
    # path('search/$', views.search, name='search')
]

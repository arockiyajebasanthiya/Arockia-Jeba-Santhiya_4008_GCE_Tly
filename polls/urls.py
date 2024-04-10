from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:question_id>/', views.detail, name='detail'),
    path('results/<int:question_id>/', views.results, name='results'),
    path('vote/<int:question_id>/', views.vote, name='vote'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]

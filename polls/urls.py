from django.urls import path
from . import views

#app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/result/', views.ResultView.as_view(), name='result'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('login_form/', views.login_form, name='login_form'),
    path('login_attempt/', views.do_login, name='do_login'),
    path('logout/', views.log_out, name='log_out')
]

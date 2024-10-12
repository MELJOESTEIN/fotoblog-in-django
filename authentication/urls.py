from django.urls import path
from . import views

urlpatterns = [
	path('', views.LoginPageView.as_view(), name='login'),
	path('signup/', views.SignupPageView.as_view(), name='signup'),
	path('logout/', views.logout_user, name='logout'),
]
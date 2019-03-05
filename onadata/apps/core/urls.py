# from .views import HomeView
from . import views
from django.conf.urls import url

urlpatterns = [
	url(r'^$', views.HomeView.as_view(), name='home'),
	url(r'project-list', views.ProjectListView.as_view(), name='project_list'),
	url(r'sign-in', views.SignInView.as_view(), name='sign_in'),
	url(r'sign-up', views.SignUpView.as_view(), name='sign_up'),
]
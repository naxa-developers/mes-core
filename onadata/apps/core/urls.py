from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.HomeView.as_view(), name='home'),
	url(r'sign-in', views.SignInView.as_view(), name='sign_in'),
	url(r'sign-up', views.SignUpView.as_view(), name='sign_up'),

	url(r'project-list', views.ProjectListView.as_view(), name='project_list'),
	url(r'project-add', views.ProjectCreateView.as_view(), name='project_add'),
	# url(r'project-edit/<int:pk>/', views.ProjectUpdateView.as_view(), name='project_edit'),
]
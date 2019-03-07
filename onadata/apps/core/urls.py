from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.HomeView.as_view(), name='home'),
	url(r'sign-in', views.SignInView.as_view(), name='sign_in'),
	url(r'sign-up', views.SignUpView.as_view(), name='sign_up'),

	url(r'project-list', views.ProjectListView.as_view(), name='project_list'),
	url(r'project-add', views.ProjectCreateView.as_view(), name='project_add'),
	url(r'^project-edit/(?P<pk>[0-9]+)/$', views.ProjectUpdateView.as_view(), name='project_edit'),
	url(r'^project-detail/(?P<pk>[0-9]+)/$', views.ProjectDetailView.as_view(), name='project_detail'),
	url(r'^project-delete/(?P<pk>[0-9]+)/$', views.ProjectDeleteView.as_view(), name='project_delete'),
]
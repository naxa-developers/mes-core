from django.conf.urls import url, include

from rest_framework.authtoken import views as restviews
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'activity', views.ActivityViewSet),
router.register(r'actgroup', views.ActivityGroupViewSet),
router.register(r'output', views.OutputViewSet),
router.register(r'project', views.ProjectViewSet),
router.register(r'cluster', views.ClusterViewSet),
router.register(r'beneficiary', views.BeneficiaryViewSet)


urlpatterns = [
	url(r'^$', views.HomeView.as_view(), name='home'),
	url(r'sign-in', views.SignInView.as_view(), name='sign_in'),
	url(r'sign-up', views.SignUpView.as_view(), name='sign_up'),

	url(r'project-list', views.ProjectListView.as_view(), name='project_list'),
	url(r'project-add', views.ProjectCreateView.as_view(), name='project_add'),
	url(r'project-edit/(?P<pk>[0-9]+)/$', views.ProjectUpdateView.as_view(), name='project_edit'),
	url(r'project-detail/(?P<pk>[0-9]+)/$', views.ProjectDetailView.as_view(), name='project_detail'),
	url(r'project-delete/(?P<pk>[0-9]+)/$', views.ProjectDeleteView.as_view(), name='project_delete'),

	url(r'output-list', views.OutputListView.as_view(), name='output_list'),
	url(r'output-detail/(?P<pk>[0-9]+)/$', views.OutputDetailView.as_view(), name='output_detail'),
	url(r'output-add', views.OutputCreateView.as_view(), name='output_add'),
	url(r'output-edit/(?P<pk>[0-9]+)/$', views.OutputUpdateView.as_view(), name='output_edit'),
	url(r'output-delete/(?P<pk>[0-9]+)/$', views.OutputDeleteView.as_view(), name='output_delete'),

	url(r'activitygroup-list', views.ActivityGroupListVeiw.as_view(), name='activitygroup_list'),
	url(r'activitygroup-detail/(?P<pk>[0-9]+)/$', views.ActivityGroupDetailView.as_view(), name='activitygroup_detail'),
	url(r'activitygroup-add', views.ActivityGroupCreateView.as_view(), name='activitygroup_add'),
	url(r'activitygroup-delete/(?P<pk>[0-9]+)/$', views.ActivityGroupDeleteView.as_view(), name='activitygroup_delete'),
	url(r'activitygroup-edit/(?P<pk>[0-9]+)/$', views.ActivityGroupUpdateView.as_view(), name='activitygroup_edit'),	

	url(r'activity-list', views.ActivityListView.as_view(), name='activity_list'),
	url(r'activity-add', views.ActivityCreateView.as_view(), name='activity_add'),
	url(r'activity-detail/(?P<pk>[0-9]+)/$', views.ActivityDetailView.as_view(), name='activity_detail'),
	url(r'activity-edit/(?P<pk>[0-9]+)/$', views.ActivityUpdateView.as_view(), name='activity_edit'),
	url(r'activity-delete/(?P<pk>[0-9]+)/$', views.ActivityDeleteView.as_view(), name='activity_delete'),

	url(r'cluster-list', views.ClusterListView.as_view(), name='cluster_list'),
	url(r'cluster-add', views.ClusterCreateView.as_view(), name='cluster_add'),
	url(r'cluster-detail/(?P<pk>[0-9]+)/$', views.ClusterDetailView.as_view(), name='cluster_detail'),
	url(r'cluster-edit/(?P<pk>[0-9]+)/$', views.ClusterUpdateView.as_view(), name='cluster_edit'),
	url(r'cluster-delete/(?P<pk>[0-9]+)/$', views.ClusterDeleteView.as_view(), name='cluster_delete'),

	url(r'beneficiary-list', views.BeneficiaryListView.as_view(), name='beneficiary_list'),
	url(r'beneficiary-add', views.BeneficiaryCreateView.as_view(), name='beneficiary_add'),
	url(r'beneficiary-detail/(?P<pk>[0-9]+)/$', views.BeneficiaryDetailView.as_view(), name='beneficiary_detail'),
	url(r'beneficiary-edit/(?P<pk>[0-9]+)/$', views.BeneficiaryUpdateView.as_view(), name='beneficiary_edit'),
	url(r'beneficiary-delete/(?P<pk>[0-9]+)/$', views.BeneficiaryDeleteView.as_view(), name='beneficiary_delete'),

	url(r'userrole-list', views.UserRoleListView.as_view(), name='userrole_list'),

	url(r'^api-token-auth/', restviews.obtain_auth_token),
]

urlpatterns += router.urls
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from rest_framework.authtoken import views as restviews
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'activity', views.ActivityViewSet),
router.register(r'actgroup', views.ActivityGroupViewSet),
router.register(r'output', views.OutputViewSet),
router.register(r'project', views.ProjectViewSet),
router.register(r'cluster', views.ClusterViewSet, base_name='Cluster'),
router.register(r'beneficiary', views.BeneficiaryViewSet),
router.register(r'config', views.ConfigViewSet),

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'sign-in', views.signin, name='sign_in'),
    url(r'sign-up', views.signup, name='sign_up'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate,
        name='activate'),
    url(r'logout', views.logout, name='logout'),
    url(r'forgot-password', views.ForgotView.as_view(), name='forgot_password'),
    url(r'404 error', views.ErrorView.as_view(), name='404_error'),
    url(r'dashboard-1', views.Dashboard1View.as_view(), name='dashboard-1'),
    url(r'dashboard-2', views.Dashboard2View.as_view(), name='dashboard-2'),
    url(r'project-dashboard', views.ProjectDashboardView.as_view(), name='project-dashboard'),

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
    url(r'my-clusters/(?P<pk>[0-9]+)/$', views.UserClusterListView.as_view(), name='user_cluster_list'),
    url(r'cluster-add', views.ClusterCreateView.as_view(), name='cluster_add'),
    url(r'cluster-detail/(?P<pk>[0-9]+)/$', views.ClusterDetailView.as_view(), name='cluster_detail'),
    url(r'cluster-edit/(?P<pk>[0-9]+)/$', views.ClusterUpdateView.as_view(), name='cluster_edit'),
    url(r'cluster-delete/(?P<pk>[0-9]+)/$', views.ClusterDeleteView.as_view(), name='cluster_delete'),
    url(r'cluster-assign/(?P<pk>[0-9]+)/$', views.ClusterAssignView.as_view(), name='cluster_assign'),

    url(r'beneficiary-list', views.BeneficiaryListView.as_view(), name='beneficiary_list'),
    url(r'beneficiary-add', views.BeneficiaryCreateView.as_view(), name='beneficiary_add'),
    url(r'beneficiary-detail/(?P<pk>[0-9]+)/$', views.BeneficiaryDetailView.as_view(), name='beneficiary_detail'),
    url(r'beneficiary-edit/(?P<pk>[0-9]+)/$', views.BeneficiaryUpdateView.as_view(), name='beneficiary_edit'),
    url(r'beneficiary-delete/(?P<pk>[0-9]+)/$', views.BeneficiaryDeleteView.as_view(), name='beneficiary_delete'),
    url(r'beneficiary-upload', views.BeneficiaryUploadView.as_view(), name='beneficiary_upload'),

    url(r'userrole-list', views.UserRoleListView.as_view(), name='userrole_list'),
    url(r'userrole-add', views.UserRoleCreateView.as_view(), name='userrole_add'),
    url(r'userrole-edit/(?P<pk>[0-9]+)/$', views.UserRoleUpdateView.as_view(), name='userrole_edit'),
    url(r'userrole-detail/(?P<pk>[0-9]+)/$', views.UserRoleDetailView.as_view(), name='userrole_detail'),
    url(r'userrole-delete/(?P<pk>[0-9]+)/$', views.UserRoleDeleteView.as_view(), name='userrole_delete'),

    url(r'config-edit/(?P<pk>[0-9]+)/$', views.ConfigUpdateView.as_view(), name='config_edit'),

    url(r'submission/(?P<pk>[0-9]+)/$', views.SubmissionView.as_view(), name='submission'),
    url(r'submission-list/(?P<pk>[0-9]+)/$', views.SubmissionListView.as_view(), name='submission_list'),

    # password_change
    url(r'^change-password/', views.change_password, name='change_password'),
    url(r'^change-password-done/', views.Done.as_view(), name='change_password_done'),

    # change status of submission
    url(r'approve', views.accept_submission, name='approve_submission'),
    url(r'reject', views.reject_submission, name='reject_submission'),

    # update target number of cluster activity
    url(r'update-cluster-act/(?P<cluster_id>[0-9]+)/(?P<pk>[0-9]+)/$', views.update_cluster_activity,
        name='update_cluster_activity'),

    url(r'^api-token-auth/', restviews.obtain_auth_token),
    url(r'^activitygroup/(?P<pk>[0-9]+)/$', views.UserActivityViewSet.as_view({'get': 'list', 'head': 'list'})),

    # reset password
    url(r'^password_reset/$', auth_views.password_reset, {
        'template_name': 'core/forgot-password.html',
        'email_template_name': 'core/password_reset_email.html',
        'subject_template_name': 'core/password_reset_subject.txt'}, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, {
        'template_name': 'core/password_reset_done.html'}, name='password_reset_done'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {'template_name': 'core/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, {'template_name': 'core/password_reset_complete.html'},
        name='password_reset_complete'),
]

urlpatterns += router.urls

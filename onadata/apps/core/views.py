from django.views.generic import View, TemplateView, ListView, DetailView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
import pandas as pd
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied, ValidationError
from itertools import chain
from rest_framework.authtoken import views as restviews
import json
from django.utils.decorators import method_decorator



from .serializers import ActivityGroupSerializer, ActivitySerializer, OutputSerializer, ProjectSerializer, \
    ClusterSerializer, BeneficiarySerialzier, ConfigSerializer, ClusterActivityGroupSerializer

from .models import Project, Output, ActivityGroup, Activity, Cluster, Beneficiary, UserRole, ClusterA, ClusterAG, Submission, Config

from .forms import SignUpForm, ProjectForm, OutputForm, ActivityGroupForm, ActivityForm, ClusterForm, BeneficiaryForm, \
    UserRoleForm, ConfigForm

from .mixin import LoginRequiredMixin, CreateView, UpdateView, DeleteView, ProjectView, ProjectRequiredMixin, \
    ProjectMixin, \
    group_required, ManagerMixin, AdminMixin


def logout_view(request):
    logout(request)

    return render()


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        if self.request.group.name in ['project-coordinator', 'social-mobilizer']:
            return HttpResponseRedirect(reverse('user_cluster_list', kwargs={'pk': self.request.user.pk}))
        elif self.request.group.name in ['project-manager', 'super-admin']:
            return render(request, self.template_name)
        else:
            raise PermissionDenied()


class SignInView(TemplateView):
    template_name = 'core/sign-in.html'


class SignUpView(TemplateView):
    template_name = 'core/sign-up.html'

    def signup(self, request):
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('core/sign-in.html')

        else:
            form = SignUpForm()
        return render(request, 'core/sign-up.html', {'form': form})


class ForgotView(TemplateView):
    template_name = 'core/forgot-password.html'


class ErrorView(TemplateView):
    template_name = 'core/404.html'


class Dashboard1View(TemplateView):
	template_name = 'core/dashboard-1.html'


class Dashboard2View(TemplateView):
	template_name = 'core/dashboard-2.html'


class ProjectListView(ListView):
	model = Project
	template_name = 'core/project-list.html'


class ProjectDetailView(ManagerMixin, DetailView):
    model = Project
    template_name = 'core/project-detail.html'


class ProjectCreateView(ManagerMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'core/project-form.html'

    success_url = reverse_lazy('project_list')


class ProjectUpdateView(ManagerMixin, UpdateView):
    model = Project
    template_name = 'core/project-form.html'
    form_class = ProjectForm
    success_url = reverse_lazy('project_list')


class ProjectDeleteView(ManagerMixin, DeleteView):
    model = Project
    template_name = 'core/project-delete.html'
    success_url = reverse_lazy('project_list')


class OutputListView(ManagerMixin, ListView):
    model = Output
    template_name = 'core/output-list.html'


class OutputDetailView(ManagerMixin, DetailView):
    model = Output
    template_name = 'core/output-detail.html'


class OutputCreateView(ManagerMixin, CreateView):
    model = Output
    template_name = 'core/output-form.html'
    form_class = OutputForm
    success_url = reverse_lazy('output_list')


class OutputUpdateView(ManagerMixin, UpdateView):
    model = Output
    template_name = 'core/output-form.html'
    form_class = OutputForm
    success_url = reverse_lazy('output_list')


class OutputDeleteView(ManagerMixin, DeleteView):
    model = Output
    template_name = 'core/output-delete.html'
    success_url = reverse_lazy('output_list')


class ActivityGroupListVeiw(ManagerMixin, ListView):
    model = ActivityGroup
    template_name = 'core/activitygroup-list.html'


class ActivityGroupDeleteView(ManagerMixin, DeleteView):
    model = ActivityGroup
    template_name = 'core/activitygroup-delete.html'
    success_url = reverse_lazy('activitygroup_list')


class ActivityGroupCreateView(ManagerMixin, CreateView):
    model = ActivityGroup
    template_name = 'core/activitygroup-form.html'
    form_class = ActivityGroupForm
    success_url = reverse_lazy('activitygroup_list')


class ActivityGroupUpdateView(ManagerMixin, UpdateView):
    model = ActivityGroup
    template_name = 'core/activitygroup-form.html'
    form_class = ActivityGroupForm
    success_url = reverse_lazy('activitygroup_list')


class ActivityGroupDetailView(ManagerMixin, DetailView):
    model = ActivityGroup
    template_name = 'core/activitygroup-detail.html'


class ActivityListView(ManagerMixin, ListView):
    model = Activity
    template_name = 'core/activity-list.html'


class ActivityCreateView(ManagerMixin, CreateView):
    model = Activity
    template_name = 'core/activity-form.html'
    form_class = ActivityForm
    success_url = reverse_lazy('activity_list')


class ActivityDetailView(ManagerMixin, DetailView):
    model = Activity
    template_name = 'core/activity-detail.html'


class ActivityUpdateView(ManagerMixin, UpdateView):
    model = Activity
    template_name = 'core/activity-form.html'
    form_class = ActivityForm
    success_url = reverse_lazy('activity_list')


class ActivityDeleteView(ManagerMixin, DeleteView):
    model = Activity
    template_name = 'core/activity-delete.html'
    success_url = reverse_lazy('activity_list')


class ClusterListView(ManagerMixin, ListView):
    model = Cluster
    template_name = 'core/cluster-list.html'
    context_object_name = 'clusters'


class UserClusterListView(LoginRequiredMixin, TemplateView):
    template_name = 'core/cluster-list.html'

    def get(self, request, **kwargs):
        user = User.objects.get(pk=kwargs.get('pk'))
        user_roles = UserRole.objects.filter(Q(user=user) & ~Q(group__name="community-social-mobilizer"))
        clusters = Cluster.objects.filter(userrole_cluster__in=user_roles)
        return render(request, self.template_name, {'clusters': clusters})


class ClusterCreateView(ManagerMixin, CreateView):
    model = Cluster
    template_name = 'core/cluster-form.html'
    form_class = ClusterForm
    success_url = reverse_lazy('cluster_list')


class ClusterDetailView(LoginRequiredMixin, DetailView):
    model = Cluster
    template_name = 'core/cluster-detail.html'


class ClusterUpdateView(ManagerMixin, UpdateView):
    model = Cluster
    template_name = 'core/cluster-form.html'
    form_class = ClusterForm
    success_url = reverse_lazy('cluster_list')


class ClusterDeleteView(ManagerMixin, DeleteView):
    model = Cluster
    template_name = 'core/cluster-delete.html'
    success_url = reverse_lazy('cluster_list')


class ClusterAssignView(ManagerMixin, View):

    def get(self, request, **kwargs):
        activity_group = ActivityGroup.objects.filter(clusterag__isnull=True)
        pk = kwargs.get('pk')
        selected_activity_group = ClusterAG.objects.filter(cluster_id=pk).select_related('activity_group')
        return render(request, 'core/cluster-assign.html',
                      {'activity_group': activity_group, 'pk': pk, 'selected_activity_group': selected_activity_group})

    def post(self, request, **kwargs):
        cluster = Cluster.objects.get(pk=kwargs.get('pk'))
        checked = [(name, value) for name, value in request.POST.iteritems()]
        for item in checked:
            if item[0].startswith('ag_'):
                item = item[0].strip('ag_')
                activity_group = ActivityGroup.objects.get(id=int(item))
                ClusterAG.objects.get_or_create(activity_group=activity_group, cluster=cluster)
            # if item[1] == 'on':
            # 	item = item[0].strip('ag_')
            # 	activity_group = ActivityGroup.objects.get(id=int(item))
            # 	ClusterAG.objects.get_or_create(activity_group=activity_group, cluster=cluster)
            # else:
            # 	item = item[0].strip('ag_')
            # 	activity_group = ActivityGroup.objects.get(id=int(item))
            # 	if ClusterAG.objects.filter(activity_group=activity_group, cluster=cluster).exists():
            # 		ClusterAG.objects.filter(activity_group=activity_group, cluster=cluster).delete()
            elif item[0].startswith('a_'):
                if item[1] == 'true':
                    item = item[0].strip('a_')
                    activity = Activity.objects.get(id=int(item))
                    # start_date = request.POST.get(str(item) + '_start_date')
                    # end_date = request.POST.get(str(item) + '_end_date')
                    cluster_ag, created = ClusterAG.objects.get_or_create(cluster=cluster,
                                                                          activity_group=activity.activity_group)
                    ClusterA.objects.get_or_create(activity=activity, cag=cluster_ag)
            # ClusterA.objects.get_or_create(activity=activity, cag=cluster_ag, start_date=start_date, end_date=end_date)
        # else:
        # 	item = item[0].strip('a_')
        # 	activity = Activity.objects.get(id=int(item))
        # 	cluster_ag, created = ClusterAG.objects.get_or_create(cluster=cluster,
        # 														  activity_group=activity.activity_group)
        # 	if ClusterA.objects.filter(activity=activity, cag=cluster_ag).exists():
        # 		ClusterA.objects.filter(activity=activity, cag=cluster_ag).delete()
        return redirect(reverse_lazy('cluster_list'))


class BeneficiaryListView(ManagerMixin, ListView):
    model = Beneficiary
    template_name = 'core/beneficiary-list.html'


class BeneficiaryCreateView(ManagerMixin, CreateView):
    model = Beneficiary
    template_name = 'core/beneficiary-form.html'
    form_class = BeneficiaryForm
    success_url = reverse_lazy('beneficiary_list')


class BeneficiaryDetailView(ManagerMixin, DetailView):
    model = Beneficiary
    template_name = 'core/beneficiary-detail.html'


class BeneficiaryUpdateView(ManagerMixin, UpdateView):
    model = Beneficiary
    template_name = 'core/beneficiary-form.html'
    form_class = BeneficiaryForm
    success_url = reverse_lazy('beneficiary_list')


class BeneficiaryDeleteView(ManagerMixin, DeleteView):
    model = Beneficiary
    template_name = 'core/beneficiary-delete.html'
    success_url = reverse_lazy('beneficiary_list')


class BeneficiaryUploadView(ManagerMixin, View):
    template_name = 'core/beneficiary-upload.html'

    def post(self, request):
        try:
            filename = request.FILES['inputFile']
            df = pd.read_excel(filename).fillna(value='')

            total = df['SN'].count()

            for row in range(0, total):
                if 'Project' in df:
                    project = Project.objects.get(id=df['Project'][row])
                else:
                    project = Project.objects.last()
                try:
                    cluster, created = Cluster.objects.get_or_create(
                        id=df['ClusterNumber'][row],
                        district=df['District'][row],
                        municipality=df['Municipality'][row],
                        ward=df['Ward'][row],
                        project=project,
                        name=df['ClusterNumber'][row])

                except:
                    cluster = Cluster.objects.get(id=df['ClusterNumber'][row])
                obj, created = Beneficiary.objects.get_or_create(
                    name=df['Name'][row],
                    ward_no=df['Ward'][row],
                    cluster=cluster,
                    address=df['Settlement'][row],
                    Type=df['Type_MPV'][row],
                    GovernmentTranch=df['GovernmentTranch'][row],
                    ConstructionPhase=df['ConstructionPhase'][row],
                    Typesofhouse=df['Typesofhouse'][row],
                    Remarks=df['Remarks'][row]
                )
            return HttpResponseRedirect('/core/beneficiary-list')
        except:
            messages.error(request, "Beneficiary upload failed. Unsupported format, or corrupt file.")
            return HttpResponseRedirect('/core/beneficiary-upload')

    def get(self, request):
        return render(request, self.template_name)


class UserRoleListView(ManagerMixin, ListView):
    model = UserRole
    template_name = 'core/userrole-list.html'


class UserRoleCreateView(ManagerMixin, CreateView):
    model = UserRole
    template_name = 'core/userrole-form.html'
    form_class = UserRoleForm
    success_url = reverse_lazy('userrole_list')


class UserRoleUpdateView(ManagerMixin, UpdateView):
    model = UserRole
    template_name = 'core/userrole-form.html'
    form_class = UserRoleForm
    success_url = reverse_lazy('userrole_list')


class UserRoleDetailView(ManagerMixin, DetailView):
    model = UserRole
    template_name = 'core/userrole-detail.html'


class UserRoleDeleteView(ManagerMixin, DeleteView):
    model = UserRole
    template_name = 'core/userrole-delete.html'
    success_url = reverse_lazy('userrole_list')


class SubmissionView(LoginRequiredMixin, View):

    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        cluster_activity_group = ClusterAG.objects.filter(cluster_id=pk)
        return render(request, 'core/submission.html', {'cluster_activity_groups': cluster_activity_group, 'pk': pk})


class SubmissionListView(LoginRequiredMixin, View):

    def get(self, request, **kwargs):
        cluster_activity = ClusterA.objects.get(pk=kwargs.get('pk'))
        submissions = Submission.objects.filter(cluster_activity=cluster_activity)
        return render(request, 'core/submission_list.html', {'submissions': submissions})


class UserRoleDeleteView(DeleteView):
    model = UserRole
    template_name = 'core/userrole-delete.html'
    success_url = reverse_lazy('userrole_list')


class SubmissionView(View):

    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        cluster_activity_group = ClusterAG.objects.filter(cluster_id=pk)
        return render(request, 'core/submission.html', {'cluster_activity_groups': cluster_activity_group, 'pk': pk})


class ConfigUpdateView(UpdateView):
	model = Config
	template_name = 'core/config-form.html'
	form_class = ConfigForm

	def get_success_url(self):
		return reverse('config_edit', kwargs={'pk': 1})

class SubmissionListView(View):

    def get(self, request, **kwargs):
        cluster_activity = ClusterA.objects.get(pk=kwargs.get('pk'))
        submissions = Submission.objects.filter(cluster_activity=cluster_activity)
        return render(request, 'core/submission_list.html', {'submissions': submissions})


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class UserActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer

    def get_queryset(self):
        roles = UserRole.objects.filter(user=self.request.user, cluster_id=self.kwargs.get('cluster_id'))
        for role in roles:
            activitygroup = ActivityGroup.objects.get(pk=self.kwargs.get('pk'))
            if role.group.name == 'social-mobilizer':
                queryset = Activity.objects.filter(activity_group=activitygroup)
            elif role.group.name == 'community-social-mobilizer':
                queryset = Activity.objects.filter(beneficiary_level=True, activity_group=activitygroup)
                print('csm')
            elif role.group.name == 'super-admin':
                queryset = Activity.objects.all()
            else:
                raise PermissionDenied()
        return queryset


class ClusterActivityGroup(viewsets.ModelViewSet):
    serializer_class = ClusterActivityGroupSerializer

    def get_queryset(self):
        cluster = Cluster.objects.filter(pk=self.kwargs.get('pk'))
        clusterag = ClusterAG.objects.filter(cluster=cluster)
        return ActivityGroup.objects.filter(clusterag__in=clusterag)


class ActivityGroupViewSet(viewsets.ModelViewSet):
    queryset = ActivityGroup.objects.all()
    serializer_class = ActivityGroupSerializer


class OutputViewSet(viewsets.ModelViewSet):
    queryset = Output.objects.all()
    serializer_class = OutputSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ClusterViewSet(viewsets.ModelViewSet):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer


class ConfigViewSet(viewsets.ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer


class BeneficiaryViewSet(viewsets.ModelViewSet):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerialzier

    def get_queryset(self):
        cluster = self.request.query_params['cluster']
        return self.queryset.filter(cluster=cluster)

class userCred(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(userCred, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return HttpResponse(json.dumps({'success': False, 'message': 'No valid request'}))

    def post(self, request):
        try:
            user_name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(username=user_name, password=pwd)
            if user is not None:
                user = User.objects.get(username=user_name)
                # user.backend = 'django.contrib.auth.backends.ModelBackend'
                # login(request, user)
                token = restviews.obtain_auth_token(request)
                user_dict = {
                    'token': "" if token is None else token.data['token'],
                    'name': user.username
                }
                userrole = UserRole.objects.filter(user=user)
                cluster = Cluster.objects.filter(userrole_cluster__in=userrole)
                cluster_arr = []
                for c in cluster:
                    cluster_arr.append(c.toDict())
                user_dict['cluster'] = cluster_arr

                return HttpResponse(json.dumps(user_dict))
            else:
                return HttpResponse(json.dumps({'success': False, 'message': 'Not a valid user'}))
        except User.DoesNotExist as e:
            return HttpResponse(json.dumps({'success': False, 'message': e.message}))

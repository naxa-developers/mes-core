from django.views.generic import View, TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
import pandas as pd
from django.contrib import messages

from .serializers import ActivityGroupSerializer, ActivitySerializer, OutputSerializer, ProjectSerializer, \
	ClusterSerializer, BeneficiarySerialzier, ConfigSerializer


from .models import Project, Output, ActivityGroup, Activity, Cluster, Beneficiary, UserRole, ClusterA, ClusterAG, Submission, Config

from .forms import SignUpForm, ProjectForm, OutputForm, ActivityGroupForm, ActivityForm, ClusterForm, BeneficiaryForm, \
				   UserRoleForm, ConfigForm


def logout_view(request):
	logout(request)

	return render()


class LoginRequiredMixin(object):
	@classmethod
	def as_view(cls, **initkwargs):
		view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
		return login_required(view)


class HomeView(LoginRequiredMixin, TemplateView):
	template_name = 'core/index.html'

	# def get(self, request, *args, **kwargs):
	# 	print(self.request.group)


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


class ProjectListView(ListView):
	model = Project
	template_name = 'core/project-list.html'


class ProjectDetailView(DetailView):
	model = Project
	template_name = 'core/project-detail.html'


class ProjectCreateView(CreateView):
	model = Project
	form_class = ProjectForm
	template_name = 'core/project-form.html'

	success_url = reverse_lazy('project_list')


class ProjectUpdateView(UpdateView):
	model = Project
	template_name = 'core/project-form.html'
	form_class = ProjectForm
	success_url = reverse_lazy('project_list')


class ProjectDeleteView(DeleteView):
	model = Project
	template_name = 'core/project-delete.html'
	success_url = reverse_lazy('project_list')


class OutputListView(ListView):
	model = Output
	template_name = 'core/output-list.html'


class OutputDetailView(DetailView):
	model = Output
	template_name = 'core/output-detail.html'


class OutputCreateView(CreateView):
	model = Output
	template_name = 'core/output-form.html'
	form_class = OutputForm
	success_url = reverse_lazy('output_list')


class OutputUpdateView(UpdateView):
	model = Output
	template_name = 'core/output-form.html'
	form_class = OutputForm
	success_url = reverse_lazy('output_list')


class OutputDeleteView(DeleteView):
	model = Output
	template_name = 'core/output-delete.html'
	success_url = reverse_lazy('output_list')


class ActivityGroupListVeiw(ListView):
	model = ActivityGroup
	template_name = 'core/activitygroup-list.html'


class ActivityGroupDeleteView(DeleteView):
	model = ActivityGroup
	template_name = 'core/activitygroup-delete.html'
	success_url = reverse_lazy('activitygroup_list')


class ActivityGroupCreateView(CreateView):
	model = ActivityGroup
	template_name = 'core/activitygroup-form.html'
	form_class = ActivityGroupForm
	success_url = reverse_lazy('activitygroup_list')


class ActivityGroupUpdateView(UpdateView):
	model = ActivityGroup
	template_name = 'core/activitygroup-form.html'
	form_class = ActivityGroupForm
	success_url = reverse_lazy('activitygroup_list')


class ActivityGroupDetailView(DetailView):
	model = ActivityGroup
	template_name = 'core/activitygroup-detail.html'


class ActivityListView(ListView):
	model = Activity
	template_name = 'core/activity-list.html'


class ActivityCreateView(CreateView):
	model = Activity
	template_name = 'core/activity-form.html'
	form_class = ActivityForm
	success_url = reverse_lazy('activity_list')


class ActivityDetailView(DetailView):
	model = Activity
	template_name = 'core/activity-detail.html'


class ActivityUpdateView(UpdateView):
	model = Activity
	template_name = 'core/activity-form.html'
	form_class = ActivityForm
	success_url = reverse_lazy('activity_list')


class ActivityDeleteView(DeleteView):
	model = Activity
	template_name = 'core/activity-delete.html'
	success_url = reverse_lazy('activity_list')


class ClusterListView(ListView):
	model = Cluster
	template_name = 'core/cluster-list.html'


class ClusterCreateView(CreateView):
	model = Cluster
	template_name = 'core/cluster-form.html'
	form_class = ClusterForm
	success_url = reverse_lazy('cluster_list')


class ClusterDetailView(DetailView):
	model = Cluster
	template_name = 'core/cluster-detail.html'


class ClusterUpdateView(UpdateView):
	model = Cluster
	template_name = 'core/cluster-form.html'
	form_class = ClusterForm
	success_url = reverse_lazy('cluster_list')


class ClusterDeleteView(DeleteView):
	model = Cluster
	template_name = 'core/cluster-delete.html'
	success_url = reverse_lazy('cluster_list')


class ClusterAssignView(View):

	def get(self, request, **kwargs):
		activity_group = ActivityGroup.objects.all()
		pk = kwargs.get('pk')
		return render(request, 'core/cluster-assign.html', {'activity_group': activity_group, 'pk': pk})

	def post(self, request, **kwargs):
		cluster = Cluster.objects.get(pk=kwargs.get('pk'))
		checked = [(name, value) for name, value in request.POST.iteritems()]
		print(checked)
		for item in checked:
			if item[0].startswith('ag_'):
				item = item[0].strip('ag_')
				activity_group = ActivityGroup.objects.get(id=int(item))
				ClusterAG.objects.get_or_create(activity_group=activity_group, cluster=cluster)
			elif item[0].startswith('a_'):
				if item[1] == 'true':
					item = item[0].strip('a_')
					activity = Activity.objects.get(id=int(item))
					cluster_ag, _ = ClusterAG.objects.get_or_create(cluster=cluster, activity_group=activity.activity_group)
					ClusterA.objects.get_or_create(activity=activity, cag=cluster_ag)
		return redirect(reverse_lazy('cluster_list'))


class BeneficiaryListView(ListView):
	model = Beneficiary
	template_name = 'core/beneficiary-list.html'


class BeneficiaryCreateView(CreateView):
	model = Beneficiary
	template_name = 'core/beneficiary-form.html'
	form_class = BeneficiaryForm
	success_url = reverse_lazy('beneficiary_list')


class BeneficiaryDetailView(DetailView):
	model = Beneficiary
	template_name = 'core/beneficiary-detail.html'


class BeneficiaryUpdateView(UpdateView):
	model = Beneficiary
	template_name = 'core/beneficiary-form.html'
	form_class = BeneficiaryForm
	success_url = reverse_lazy('beneficiary_list')


class BeneficiaryDeleteView(DeleteView):
	model = Beneficiary
	template_name = 'core/beneficiary-delete.html'
	success_url = reverse_lazy('beneficiary_list')


class BeneficiaryUploadView(View):
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

class UserRoleListView(ListView):
	model = UserRole
	template_name = 'core/userrole-list.html'


class UserRoleCreateView(CreateView):
	model = UserRole
	template_name = 'core/userrole-form.html'
	form_class = UserRoleForm
	success_url = reverse_lazy('userrole_list')


class UserRoleUpdateView(UpdateView):
	model = UserRole
	template_name = 'core/userrole-form.html'
	form_class = UserRoleForm
	success_url = reverse_lazy('userrole_list')


class UserRoleDetailView(DetailView):
	model = UserRole
	template_name = 'core/userrole-detail.html'


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
	success_url = reverse_lazy('')


class SubmissionListView(View):

	def get(self, request, **kwargs):
		cluster_activity = ClusterA.objects.get(pk=kwargs.get('pk'))
		submissions = Submission.objects.filter(cluster_activity=cluster_activity)
		return render(request, 'core/submission_list.html', {'submissions': submissions})



class ActivityViewSet(viewsets.ModelViewSet):
	queryset = Activity.objects.all()
	serializer_class = ActivitySerializer


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



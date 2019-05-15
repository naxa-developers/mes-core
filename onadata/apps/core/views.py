from django.views.generic import View, TemplateView, ListView, DetailView
from django.contrib.auth import views
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from django.contrib.gis.geos import Point

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, views
import pandas as pd
from django.db.models import Q
from django.db.models import Avg, Count, Sum
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied, ValidationError
from itertools import chain
from rest_framework.authtoken import views as restviews
import json
from django.utils.decorators import method_decorator
from datetime import datetime
from django.db import transaction
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .signup_tokens import account_activation_token
from django.views.generic.list import MultipleObjectMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.core.serializers import serialize


from onadata.apps.logger.models import Instance
from .serializers import ActivityGroupSerializer, ActivitySerializer, OutputSerializer, ProjectSerializer, \
    ClusterSerializer, BeneficiarySerialzier, ConfigSerializer, ClusterActivityGroupSerializer, CASerializer

from .models import Project, Output, ActivityGroup, Activity, Cluster, Beneficiary, UserRole, ClusterA, ClusterAG, \
    Submission, Config, ProjectTimeInterval, ClusterAHistory, District, Municipality

from .forms import LoginForm, SignUpForm, ProjectForm, OutputForm, ActivityGroupForm, ActivityForm, ClusterForm, \
    BeneficiaryForm, UserRoleForm, ConfigForm, ChangePasswordform

from .mixin import LoginRequiredMixin, CreateView, UpdateView, DeleteView, ProjectView, ProjectRequiredMixin, \
    ProjectMixin, group_required, ManagerMixin, AdminMixin

from .utils import get_beneficiaries, get_clusters, get_cluster_activity_data, get_progress_data

def logout_view(request):
    logout(request)

    return HttpResponseRedirect('/core/sign-in/')


class HomeView(LoginRequiredMixin, TemplateView):    
    template_name = 'core/index.html'

    def get(self, request):
        if self.request.group.name in ['project-coordinator', 'social-mobilizer']:
            return HttpResponseRedirect(reverse('user_cluster_list', kwargs={'pk': self.request.user.pk}))
        elif self.request.group.name in ['project-manager', 'super-admin', 'project-management-unit']:
            
            output_count = Output.objects.all().count()
            activity_count = Activity.objects.all().count()
            ag_count = ActivityGroup.objects.all().count()     
            cluster = Cluster.objects.all().count()    
            beneficiary = Beneficiary.objects.all().count()   
            context = {
                'output_count': output_count,
                'activity_count': activity_count,
                'ag_count': ag_count,
                'cluster': cluster,
                'beneficiary': beneficiary
            }
            return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect(reverse('404_error'))
            # raise PermissionDenied()

    # def get_context_data(request, **kwargs):
    #     import ipdb
    #     ipdb.set_trace()

    #     context = super(HomeView, self).get_context_data(**kwargs)

    #     output = Output.objects.all()
    #     output_count = Output.objects.all().count()
    #     context['output'] = output
    #     context['output_count'] = output_count
    #     print(context)
    #     return context


class ProjectDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/project-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


class ProjectDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/project-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        output = Output.objects.all()
        context['output'] = output
        return context


def web_authenticate(username=None, password=None):
    try:
        if "@" in username:
            user = User.objects.get(email__iexact=username)
        else:
            user = User.objects.get(username__iexact=username)
        if user.check_password(password):
            return authenticate(username=user.username, password=password), False
        else:
            return None, True  # Email is correct
    except User.DoesNotExist:
        return None, False  # false Email incorrect


def signin(request):
    if request.user.is_authenticated():
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            user, valid_email = web_authenticate(username=username, password=pwd)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    return render(request, 'core/sign-in.html',
                                  {'form': form,
                                   'email_error': "Your Account is Deactivated, Please Contact Administrator.",
                                   'valid_email': valid_email,
                                   'login_username': username
                                   })
            else:
                if valid_email:
                    email_error = False
                    password_error = True
                else:
                    password_error = False
                    email_error = "Invalid Username, please check your username."
                return render(request, 'core/sign-in.html',
                              {'form': form,
                               'valid_email': valid_email,
                               'email_error': email_error,
                               'password_error': password_error,
                               'login_username': username
                               })
        else:
            if request.POST.get('login_username') is not None:
                login_username = request.POST.get('login_username')
            else:
                login_username = ''
            return render(request, 'core/sign-in.html', {
                'form': form,
                'valid_email': False,
                'email_error': "Your username and password did not match.",
                'login_username': login_username
            })
    else:
        form = LoginForm()

    return render(request, 'core/sign-in.html', {'form': form, 'valid_email': True, 'email_error': False})


def signup(request):
    if request.user.is_authenticated():
        return redirect('/core')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = User.objects.create(username=username, email=email, password=password)
            user.set_password(user.password)
            user.is_active = False
            user.save()

            mail_subject = 'Activate your account.'
            current_site = get_current_site(request)
            message = render_to_string('core/acc_active_email.html', {
                'user': user,
                'domain': settings.SITE_URL,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'core/emailnotify.html', {'email': user.email})

        else:
            username = request.POST.get('username')
            email = request.POST.get('email')
            return render(request, 'core/sign-up.html', {
                'form': form,
                'username': username,
                'email': email,
                'valid_email': True,
                'email_error': False
            })
    else:
        form = SignUpForm()
        return render(request, 'core/sign-up.html', {
            'form': form,
            'valid_email': True,
            'email_error': False
        })


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        return redirect(reverse_lazy('sign_in'))
    else:
        return HttpResponse('Activation link is invalid!')


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

    def get(self, request):
        activity_groups = ActivityGroup.objects.filter(project=request.project)
        activities = Activity.objects.filter(activity_group__project=request.project)
        districts = District.objects.all()
        municipalities = Municipality.objects.all()
        select_cluster = Cluster.objects.filter(project=request.project)
        types = Beneficiary.objects.values('Type').distinct('Type')
        intervals = ProjectTimeInterval.objects.values('label').order_by('label')
        beneficiary_count = Beneficiary.objects.count()
        activity_count = Activity.objects.count()
        interval = []

        for item in intervals:
            interval.append(str(item['label']))

        pie_data = {}
        beneficiary_types = Beneficiary.objects.filter(cluster__project=request.project).values('Type').\
            distinct().annotate(total=Count('Type'))
        for item in beneficiary_types:
            pie_data[str(item['Type'])] = [round((float(item['total']) / 1500) * 100, 2)]

        # get cluster activity overview data on basis of filter used
        if 'cluster_activity' in request.GET:
            checked = [(name, value) for name, value in request.GET.iteritems()]
            activity_group = []
            activity = []
            for item in checked:
                if item[0].startswith('a'):
                    activity.append(item[0].split("_")[1])

            chart_single = get_cluster_activity_data(request.project, activity)

        # for no filter used
        else:
            chart_single = get_cluster_activity_data(request.project)

        # get progress overview data on basis of filter used
        if 'progress' in request.GET:
            checked = [(name, value) for name, value in request.GET.iteritems()]
            clusters = []
            select_districts = []
            munis = []
            for item in checked:
                if item[0].startswith('cl'):
                    clusters.append(int(item[0].split("_")[1]))

                if item[0].startswith('mun'):
                    munis.append(int(item[0].split("_")[1]))

                if item[0].startswith('dist'):
                    select_districts.append(int(item[0].split("_")[1]))

            progress_data, categories, cluster_progress_data = get_progress_data(
                request.project, types, clusters, select_districts, munis)

        else:
            progress_data, categories, cluster_progress_data = get_progress_data(request.project, types)

        return render(request, self.template_name, {
            'activity_groups': activity_groups,
            'activities': activities,
            'districts': districts,
            'municipalities': municipalities,
            'select_clusters': select_cluster,
            'types': types,
            'activity_count': activity_count,
            'beneficiary_count': beneficiary_count,
            'intervals': interval,
            'chart_single': chart_single,
            'progress_data': progress_data,
            'cluster_progress_data': cluster_progress_data,
            'pie_data': pie_data,
            'categories': categories
        })


# for map data
def get_map_data(request):
    if request.is_ajax():
        clusters = Cluster.objects.filter(project=request.project)
        # beneficiaries = []
        # for item in ca:
        #     if item.activity.beneficiary_level:
        #         cluster = Cluster.objects.filter(id=item.cag.cluster.id)
        #         beneficiaries.append(*Beneficiary.objects.filter(cluster__in=cluster))
        activities = ClusterA.objects.filter(
            cag__cluster__in=clusters, activity__beneficiary_level=False)

        data = serialize(
            'geojson',
            activities,
            geometry_field='location',
            fields=('activity', 'location', 'target_number', 'target_completed'),
        )
        print(data)
        return HttpResponse(data)


class Dashboard2View(MultipleObjectMixin, TemplateView):
    template_name = 'core/dashboard-2.html'

    def get(self, request):
        checked = [(name, value) for name, value in request.GET.iteritems()]
        clusters = []
        b_types = []
        districts = []
        munis = []
        for item in checked:
            if item[0].startswith('cl'):
                clusters.append(int(item[0].split("_")[1]))

            if item[0].startswith('tp'):
                b_types.append(item[0].split("_")[1])

            if item[0].startswith('mun'):
                munis.append(int(item[0].split("_")[1]))

            if item[0].startswith('dist'):
                districts.append(int(item[0].split("_")[1]))

        beneficiaries = get_beneficiaries(districts, munis, clusters, b_types)

        ag = ActivityGroup.objects.all()

        # page = request.GET.get('page', 1)
        # paginator = Paginator(beneficiaries, 100)
        #
        # try:
        #     beneficiaries = paginator.page(page)
        # except PageNotAnInteger:
        #     beneficiaries = paginator.page(1)
        # except EmptyPage:
        #     beneficiaries = paginator.page(paginator.num_pages)

        districts = District.objects.all()
        municipalities = Municipality.objects.all()
        cluster = Cluster.objects.all()
        types = Beneficiary.objects.values('Type').distinct('Type')
        return render(request, self.template_name, {
            'activity_groups': ag, 
            'beneficiaries': beneficiaries, 
            'districts': districts, 
            'municipalities': municipalities,
            'clusters': cluster,
            'types': types
        })


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

    def get_form_kwargs(self):
        kwargs = super(ActivityCreateView, self).get_form_kwargs()
        kwargs['project'] = self.request.project
        return kwargs


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
        pk = kwargs.get('pk')
        clusterag = ClusterAG.objects.filter(cluster_id=pk)
        activity_group = ActivityGroup.objects.filter(~Q(clusterag__in=clusterag))
        selected_activity_group = ClusterAG.objects.filter(cluster_id=pk).select_related('activity_group')
        time_interval = ProjectTimeInterval.objects.filter(project=request.project)
        return render(request, 'core/cluster-assign.html',
                      {
                          'activity_group': activity_group,
                          'pk': pk,
                          'selected_activity_group': selected_activity_group,
                          'interval': time_interval
                      })

    @transaction.atomic
    def post(self, request, **kwargs):
        cluster = Cluster.objects.get(pk=kwargs.get('pk'))
        checked = [(name, value) for name, value in request.POST.iteritems()]
        print(checked)
        for item in checked:
            if item[0].startswith('ag_'):
                item = item[0].strip('ag_')
                activity_group = ActivityGroup.objects.get(id=int(item))
                ClusterAG.objects.get_or_create(
                    activity_group=activity_group,
                    cluster=cluster
                )
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
                    cluster_ag, created = ClusterAG.objects.get_or_create(cluster=cluster,
                                                                          activity_group=activity.activity_group)
                    ca, created = ClusterA.objects.get_or_create(
                        activity=activity,
                        cag=cluster_ag
                    )
                    if not ca.activity.beneficiary_level:
                        for check in checked:
                            if not created:
                                hist = ClusterAHistory()
                                ca.target_unit = ca.activity.target_unit
                                longitude = ''
                                latitude = ''

                                val = 'lat_' + item
                                if check[0] == val:
                                    latitude = check[1]

                                val = 'long_' + item
                                if check[0] == val:
                                    longitude = check[1]

                                val = 'target_' + item
                                if check[0] == val:
                                    if ',' in check[1]:
                                        value = check[1].replace(',', '')
                                        if not ca.target_number == int(value):
                                            hist.clustera = ca
                                            hist.target_number = ca.target_number
                                            hist.target_completed = ca.target_completed
                                            hist.time_interval = ca.time_interval
                                            hist.updated_date = datetime.now()
                                            hist.save()
                                            ca.target_number = check[1]
                                            ca.target_updated = True
                                    else:
                                        if not ca.target_number == int(check[1]):
                                            hist.clustera = ca
                                            hist.target_number = ca.target_number
                                            hist.target_completed = ca.target_completed
                                            hist.time_interval = ca.time_interval
                                            hist.updated_date = datetime.now()
                                            hist.save()
                                            ca.target_number = check[1]
                                            ca.target_updated = True

                                val = 'interval_' + item
                                if check[0] == val:
                                    if not ca.time_interval == ProjectTimeInterval.objects.get(id=int(check[1])):
                                        hist.clustera = ca
                                        hist.time_interval = ca.time_interval
                                        hist.target_number = ca.target_number
                                        hist.target_completed = ca.target_completed
                                        hist.updated_date = datetime.now()
                                        hist.save()
                                        ca.time_interval = ProjectTimeInterval.objects.get(id=int(check[1]))
                                        ca.interval_updated = True

                                if longitude != '':
                                    ca.location = Point(
                                        round(float(longitude), 6),
                                        round(float(ca.latitude.real if ca.latitude else "27.7172"), 6),
                                        srid=4326)

                                if latitude != '':
                                    ca.location = Point(
                                        round(float(ca.longitude.real if ca.longitude else "85.3240"), 6),
                                        round(float(latitude), 6),
                                        srid=4326)
                                ca.save()
                            else:
                                longitude = ''
                                latitude = ''
                                val = 'lat_' + item
                                if check[0] == val:
                                    latitude = check[1]

                                val = 'long_' + item
                                if check[0] == val:
                                    longitude = check[1]

                                val = 'target_' + item
                                if check[0] == val:
                                    if ',' in check[1]:
                                        value = check[1].replace(',', '')
                                        ca.target_number = int(value)
                                    else:
                                        ca.target_number = int(check[1])

                                val = 'interval_' + item
                                if check[0] == val:
                                    ca.time_interval = ProjectTimeInterval.objects.get(id=int(check[1]))

                                if longitude != '':
                                    ca.location = Point(
                                        round(float(longitude), 6),
                                        round(float(ca.latitude.real if ca.latitude else "27.7172"), 6),
                                        srid=4326)

                                if latitude != '':
                                    ca.location = Point(
                                        round(float(ca.longitude.real if ca.longitude else "85.3240"), 6),
                                        round(float(latitude), 6),
                                        srid=4326)
                                ca.save()

                    else:
                        for check in checked:
                            if not created:
                                val = 'interval_' + item
                                if check[0] == val:
                                    if not ca.time_interval == ProjectTimeInterval.objects.get(id=int(check[1])):
                                        ClusterAHistory.objects.get_or_create(
                                            clustera=ca, time_interval=ca.time_interval, updated_date=datetime.now())
                                        ca.time_interval = ProjectTimeInterval.objects.get(id=int(check[1]))
                                        ca.interval_updated = True
                                        ca.save()
                            else:
                                val = 'interval_' + item
                                if check[0] == val:
                                    ca.time_interval = ProjectTimeInterval.objects.get(id=int(check[1]))
                                    ca.save()
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

                district, created = District.objects.get_or_create(name=df['District'][row])
                municipality, created = Municipality.objects.get_or_create(
                    district=district, name=df['Municipality'][row])
                try:
                    cluster, created = Cluster.objects.get_or_create(
                        id=df['ClusterNumber'][row],
                        ward=df['Ward'][row],
                        project=project,
                        name=df['ClusterNumber'][row])
                    cluster.municipality.add(municipality)
                    cluster.save()
                # capture integrity constraint exception if any field name is incorrect
                # for a cluster with already existing cluster number
                except:
                    cluster = Cluster.objects.get(id=df['ClusterNumber'][row])
                    cluster.municipality.add(municipality)
                    cluster.save()
                Beneficiary.objects.get_or_create(
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
        except Exception as e:
            print(e)
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
        time_interval = ProjectTimeInterval.objects.filter(project=request.project)
        return render(request, 'core/submission.html', {
            'cluster_activity_groups': cluster_activity_group,
            'pk': pk,
            'interval': time_interval
        })


class SubmissionListView(LoginRequiredMixin, View):

    def get(self, request, **kwargs):
        cluster_activity = ClusterA.objects.get(pk=kwargs.get('pk'))
        submissions = Submission.objects.filter(cluster_activity=cluster_activity)
        return render(request, 'core/submission_list.html', {'submissions': submissions, 'activity': cluster_activity})


class SubNotificationListView(LoginRequiredMixin, View):

    def get(self, request, **kwargs):
        submissions = Submission.objects.all().order_by('instance__date_created')
        return render(request, 'core/submission_notification.html', {'submissions': submissions})


class ConfigUpdateView(UpdateView):
    model = Config
    template_name = 'core/config-form.html'
    form_class = ConfigForm

    def get_success_url(self):
        return reverse('config_edit', kwargs={'pk': 1})


def accept_submission(request):
    submission = Submission.objects.get(pk=request.GET.get('pk'))
    submission.status = 'approved'
    submission.save()
    return HttpResponseRedirect(reverse('submission_list', kwargs={'pk': request.GET.get('clustera_id')}))


def reject_submission(request):
    submission = Submission.objects.get(pk=request.GET.get('pk'))
    submission.status = 'rejected'
    submission.save()

    to_email = submission.instance.user.email
    mail_subject = 'Submission Rejected.'
    message = render_to_string('core/submission_reject_email.html', {
        'submission': submission.instance,
        'rejected_by': request.user.username,
        'activity': submission.cluster_activity.activity.name,
        'cluster': submission.cluster_activity.cag.cluster.name,
        'date': datetime.now(),
    })
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    return HttpResponseRedirect(reverse('submission_list', kwargs={'pk': request.GET.get('clustera_id')}))


@transaction.atomic
def update_cluster_activity(request, **kwargs):
    pk = kwargs.get('pk')
    ca = ClusterA.objects.get(pk=pk)
    target_number = request.POST.get('target_number')
    cahistory = ClusterAHistory()
    if target_number is not None:
        if not ca.target_completed == float(target_number):
            print(ca.target_completed, target_number)
            cahistory.clustera = ca
            cahistory.target_number = ca.target_number
            cahistory.time_interval = ca.time_interval
            cahistory.target_completed = ca.target_completed
            cahistory.updated_date = datetime.now()
            cahistory.save()
            ca.target_completed = target_number
            ca.save()

    return HttpResponseRedirect(reverse('submission', kwargs={'pk': kwargs.get('cluster_id')}))


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class UserActivityViewSet(viewsets.ModelViewSet):
    serializer_class = CASerializer

    def get_queryset(self):
        role = self.request.user.user_roles.first()
        activitygroup = ClusterAG.objects.get(pk=self.kwargs.get('pk'))
        if role.group.name == 'social-mobilizer':
            queryset = ClusterA.objects.filter(cag=activitygroup)
        elif role.group.name == 'community-social-mobilizer':
            queryset = ClusterA.objects.filter(activity__beneficiary_level=True, cag=activitygroup)
        elif role.group.name == 'super-admin':
            queryset = ClusterA.objects.all()
        else:
            return HttpResponseRedirect(reverse('404_error'))
            # raise PermissionDenied()
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
    serializer_class = ClusterSerializer

    def get_queryset(self):
        roles = self.request.user.user_roles.all()
        if len(roles) > 1:
            cluster = Cluster.objects.filter(userrole_cluster__in=roles)
        else:
            cluster = Cluster.objects.filter(userrole_cluster=self.request.role)
        return cluster


class ConfigViewSet(viewsets.ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer


class BeneficiaryViewSet(viewsets.ModelViewSet):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerialzier

    def get_queryset(self):
        cluster = self.request.query_params['cluster']
        return self.queryset.filter(cluster=cluster)


class BeneficiaryTypeView(views.APIView):

    def get(self, request):
        pie_data = {}
        types = Beneficiary.objects.filter(cluster__project=request.project).values('Type').\
            distinct().annotate(total=Count('Type'))
        for item in types:
            pie_data[item['Type']] = [round((float(item['total']) / 1500) * 100, 2)]

        return Response(pie_data)


# class userCred(View):
#
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super(userCred, self).dispatch(request, *args, **kwargs)
#
#     def get(self, request):
#         return HttpResponse(json.dumps({'success': False, 'message': 'No valid request'}))
#
#     def post(self, request):
#         try:
#             user_name = request.POST.get('username')
#             pwd = request.POST.get('password')
#             user = authenticate(username=user_name, password=pwd)
#             if user is not None:
#                 user = User.objects.get(username=user_name)
#                 # user.backend = 'django.contrib.auth.backends.ModelBackend'
#                 # login(request, user)
#                 token = restviews.obtain_auth_token(request)
#                 userrole = UserRole.objects.filter(user=user)
#                 user_dict = {
#                     'token': "" if token is None else token.data.get('token'),
#                     'name': user.username,
#                 }
#                 cluster = Cluster.objects.filter(userrole_cluster__in=userrole).prefetch_related('userrole_cluster')
#                 cluster_arr = []
#                 for c in cluster:
#                     group = c.userrole_cluster.first().group.name
#                     c_dict = c.toDict()
#                     c_dict['role'] = group
#                     cluster_arr.append(c_dict)
#                 user_dict['cluster'] = cluster_arr
#
#                 return HttpResponse(json.dumps(user_dict))
#             else:
#                 return HttpResponseBadRequest()
#         except User.DoesNotExist as e:
#             return HttpResponse(json.dumps({'message': e.message}))


class Done(TemplateView):
   template_name = 'core/change-password-done.html'


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordform(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            # messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password_done')

    else:
        form = ChangePasswordform(request.user)
    return render(request, 'core/change-password.html', {
        'form': form
    })


def get_municipalities(request):
    if request.is_ajax():
        districts = request.GET.getlist('districts[]')
        if districts:
            municipalities = Municipality.objects.filter(district_id__in=districts)
            municipalities = serialize("json", municipalities)
            return HttpResponse(municipalities)
        else:
            municipalities = Municipality.objects.all()
            municipalities = serialize("json", municipalities)
            return HttpResponse(municipalities)
    else:
        return HttpResponse('not ajax request')


def get_clusters(request):
    if request.is_ajax():
        municipalities = request.GET.getlist('municipalities[]')
        if municipalities:
            clusters = Cluster.objects.filter(municipality__id__in=municipalities).distinct()
            clusters = serialize("json", clusters)
            print(clusters)
            return HttpResponse(clusters)
        else:
            clusters = Cluster.objects.all()
            clusters = serialize("json", clusters)
            return HttpResponse(clusters)
    else:
        return HttpResponse('not ajax request')


def get_activity_group(request):
    if request.is_ajax():
        clusters = request.GET.getlist('clusters[]')
        print(clusters)
        if clusters:
            print('inside clusters', clusters)
            cluster_activity_groups = ClusterAG.objects.filter(cluster_id__in=clusters)
            if cluster_activity_groups:
                cluster_activity_groups_list = []
                for item in cluster_activity_groups:
                    cluster_activity_groups_list.append(item.activity_group.id)
                activity_groups = ActivityGroup.objects.filter(id__in=cluster_activity_groups_list)
                activity_groups = serialize("json", activity_groups)
                return HttpResponse(activity_groups)
            else:
                activity_groups = ActivityGroup.objects.all()
                activity_groups = serialize("json", activity_groups)
                return HttpResponse(activity_groups)
        else:
            activity_groups = ActivityGroup.objects.all()
            activity_groups = serialize("json", activity_groups)
            return HttpResponse(activity_groups)
    else:
        return HttpResponse('not ajax request')


def get_activity(request):
    if request.is_ajax():
        activity_groups = request.GET.getlist('activity_groups[]')
        if activity_groups:
            activity = Activity.objects.filter(activity_group_id__in=activity_groups)
            activity = serialize("json", activity)
            return HttpResponse(activity)
        else:
            activity = Activity.objects.all()
            activity = serialize("json", activity)
            return HttpResponse(activity)
    else:
        return HttpResponse('not ajax request')

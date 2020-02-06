from django.views.generic import View, TemplateView, ListView, DetailView
from django.contrib.auth import views
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.template import RequestContext
from django.utils.translation import ugettext as _
from onadata.libs.utils.viewer_tools import enketo_url

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
import json
import ast
from django.contrib.gis.geos import Point

from onadata.apps.logger.models import Instance, XForm
from .serializers import ActivityGroupSerializer, ActivitySerializer, OutputSerializer, ProjectSerializer, \
    ClusterSerializer, BeneficiarySerialzier, ConfigSerializer, ClusterActivityGroupSerializer, CASerializer

from .models import Project, Output, ActivityGroup, Activity, Cluster, Beneficiary, UserRole, ClusterA, ClusterAG, \
    Submission, Config, ProjectTimeInterval, ClusterAHistory, District, Municipality, ActivityAggregate, ActivityAggregateHistory

from .forms import LoginForm, SignUpForm, ProjectForm, OutputForm, ActivityGroupForm, ActivityForm, ClusterForm, \
    BeneficiaryForm, UserRoleForm, ConfigForm, ChangePasswordform

from .mixin import LoginRequiredMixin, CreateView, UpdateView, DeleteView, ProjectView, ProjectRequiredMixin, \
    ProjectMixin, group_required, ManagerMixin, AdminMixin

from .utils import get_beneficiaries, get_clusters, get_cluster_activity_data, get_progress_data, \
    get_form_location_label, image_urls_dict, inject_instanceid, create_db_table

from onadata.libs.utils.viewer_tools import _get_form_url


def logout_view(request):
    logout(request)

    return HttpResponseRedirect('/core/sign-in/')


class HomeView(LoginRequiredMixin, TemplateView):    
    template_name = 'core/index.html'

    def get(self, request):
        if self.request.group.name in ['project-coordinator', 'social-mobilizer']:
            return HttpResponseRedirect(reverse('user_cluster_list', kwargs={'pk': self.request.user.pk}))
        elif self.request.group.name in ['project-manager', 'project-management-unit']:
            
            output_count = Output.objects.filter(project=self.request.project).count()
            activity_count = Activity.objects.filter(activity_group__project=self.request.project).count()
            ag_count = ActivityGroup.objects.filter(project=self.request.project).count()     
            cluster = Cluster.objects.filter(project=self.request.project).count()    
            beneficiary = Beneficiary.objects.filter(cluster__project=self.request.project).count()   
            context = {
                'output_count': output_count,
                'activity_count': activity_count,
                'ag_count': ag_count,
                'cluster': cluster,
                'beneficiary': beneficiary
            }
            return render(request, self.template_name, context)
        elif self.request.group.name in ['super-admin', ]:
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
                    if user.user_roles.first().group.name == 'project-manager':
                        return HttpResponseRedirect(reverse('dashboard-1'))
                    else:
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


class ForgotView(TemplateView):
    template_name = 'core/forgot-password.html'


class ErrorView(TemplateView):
    template_name = 'core/404.html'


class DashboardNewView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard-1new.html'

    def get(self, request):
        project = request.project
        beneficiary_count = Beneficiary.objects.filter(cluster__project=project).count()
        activity_count = Activity.objects.filter(activity_group__project=project).count()
        districts = District.objects.filter(beneficiary__isnull=False).distinct()

        script_district_queryset = District.objects.filter(beneficiary__isnull=False).distinct().values('id', 'name')
        script_district = json.dumps(list(script_district_queryset))
        return render(request, self.template_name, {
            'activity_count': activity_count, 
            'beneficiary_count': beneficiary_count,
            'districts': districts,
            'script_district': script_district})


def get_district_progress(request):
    district = District.objects.get(pk=request.GET.get('id'))
    types = Beneficiary.objects.filter(district=district, cluster__project=request.project).values('Type').distinct()
    progress_data = {}
    categories = []

    project=request.project
    
    for item in types:
        beneficiary_progress = 0
        total_dict = {}
        if 'request_data[]' in request.GET:
            municipalities = request.GET.getlist('request_data[]')
            for municipality in municipalities:
                beneficiary = Beneficiary.objects.filter(municipality__id=int(municipality), Type=item['Type'], cluster__project=project)
                for obj in beneficiary:
                    try:
                        beneficiary_progress += obj.progress
                    except:
                        beneficiary_progress += 1
                total_dict['sum'] = beneficiary_progress
                total_dict['total'] = len(beneficiary)
                progress_data[item['Type']] = total_dict
        else:
            beneficiary = Beneficiary.objects.filter(district=district, Type=item['Type'], cluster__project=project)
            for obj in beneficiary:
                try:
                    beneficiary_progress += obj.progress
                except:
                    beneficiary_progress += 1
            total_dict['sum'] = beneficiary_progress
            total_dict['total'] = len(beneficiary)
            progress_data[item['Type']] = total_dict
    return JsonResponse(progress_data)

def get_phase_data(request, *args, **kwargs):
    project = request.project
    types = Beneficiary.objects.filter(cluster__project=project)
    construction_phases = {}
    data = []
    if 'district' in request.GET:
        district = District.objects.get(id=int(request.GET.get('district')))
        activity_groups = ActivityGroup.objects.filter(project=project, output__name='House Construction', clusterag__cluster__municipality__district=district).distinct()
        print(activity_groups)
        for ag in activity_groups:
            total_dict = {}
            beneficiaries = 0
            phases = []
            activities = Activity.objects.filter(activity_group=ag)
            beneficiary = Beneficiary.objects.filter(district=district, submissions__cluster_activity__cag__activity_group=ag)
            for item in beneficiary:
                completed = True
                for activity in activities:
                    if Submission.objects.filter(beneficiary=item, cluster_activity__activity=activity, status="pending").exists():
                        completed = False
                if completed:
                    beneficiaries += 1
            ben = round((float(beneficiaries) / len(beneficiary) * 100), 2)
            total_dict['sum'] = ben
            total_dict['number'] = beneficiaries
            total_dict['total'] = round((float(beneficiaries) / len(types)) * 100, 2)
            construction_phases[ag.name] = total_dict
    else:
        activity_groups = ActivityGroup.objects.filter(project=project, output__name='House Construction')
        for ag in activity_groups:
            total_dict = {}
            beneficiaries = 0
            phases = []
            activities = Activity.objects.filter(activity_group=ag)
            beneficiary = Beneficiary.objects.filter(submissions__cluster_activity__cag__activity_group=ag)
            for item in beneficiary:
                completed = True
                for activity in activities:
                    if Submission.objects.filter(beneficiary=item, cluster_activity__activity=activity, status="pending").exists():
                        completed = False
                if completed:
                    beneficiaries += 1
            ben = round((float(beneficiaries) / len(beneficiary) * 100), 2)
            total_dict['sum'] = ben
            total_dict['number'] = beneficiaries
            total_dict['total'] = round((float(beneficiaries) / len(types)) * 100, 2)
            construction_phases[ag.name] = total_dict
    return JsonResponse(construction_phases)


class Dashboard1View(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard-1.html'

    def get(self, request):
        project = request.project
        # data required for charts and drop down menus
        districts = District.objects.filter(id__in=Beneficiary.objects.values('district__id').distinct())
        municipalities = Municipality.objects.filter(id__in=Beneficiary.objects.values('municipality__id').distinct())
        select_cluster = Cluster.objects.filter(project=project)

        types = Beneficiary.objects.filter(cluster__project=project).values('Type').distinct()
        # intervals = ProjectTimeInterval.objects.values('label').order_by('label')
        beneficiary_count = Beneficiary.objects.filter(cluster__project=project).count()
        activity_count = Activity.objects.filter(activity_group__project=project).count()
        interval = []

        # time intervals for activity progress data
        # for item in intervals:
        #     interval.append(str(item['label']))

        # for beneficiary type pie data
        pie_data = {}
        beneficiary_types = types.annotate(total=Count('Type'))
        for item in beneficiary_types:
            pie_data[str(item['Type'])] = [round((float(item['total']) / beneficiary_count) * 100, 2)]

        # get cluster activity overview data on basis of filter used
        # if 'cluster_activity' in request.GET:
        #     checked = [(name, value) for name, value in request.GET.iteritems()]
        #     activity = []
        #     for item in checked:
        #         if item[0].startswith('a'):
        #             activity.append(item[0].split("_")[1])

        #     chart_single = get_cluster_activity_data(request.project, activity)

        # for no filter used
        # else:
        #     chart_single = get_cluster_activity_data(request.project)

        # get progress overview data on basis of filter used
        # if 'progress' in request.GET:
        #     checked = [(name, value) for name, value in request.GET.iteritems()]
        #     clusters = []
        #     select_districts = []
        #     munis = []
        #     for item in checked:
        #         if item[0].startswith('cl'):
        #             clusters.append(int(item[0].split("_")[1]))

        #         if item[0].startswith('mun'):
        #             munis.append(int(item[0].split("_")[1]))

        #         if item[0].startswith('dist'):
        #             select_districts.append(int(item[0].split("_")[1]))

        #     construction_phases = get_progress_data(
        #         request.project, types, clusters, select_districts, munis)

        # else:
        #     construction_phases = get_progress_data(request.project, types)

        return render(request, self.template_name, {
            'districts': districts,
            'municipalities': municipalities,
            'select_clusters': select_cluster,
            'activity_count': activity_count,
            'beneficiary_count': beneficiary_count,
            # 'intervals': interval,
            # 'chart_single': chart_single,
            'pie_data': pie_data,
            # 'construction_phases': construction_phases
        })


def get_answer(json, labels):
    value = []
    for label in labels:
        if label in json:
            value.append(json[label])
    return value


# for map data in dashboard1
def get_map_data(request):
    project = request.project
    form = XForm.objects.get(id_string='aLXbstTLbCJn8eQqDbbaQg')
    form_json = form.json
    labels = get_form_location_label(json.loads(form_json))

    instances = Instance.objects.filter(xform_id=form.id)
    for instance in instances:
        instance_json = instance.json
        instance_json = ast.literal_eval(str(instance_json))
        answers = get_answer(instance_json, labels)
        beneficiary = Beneficiary.objects.filter(submissions__instance=instance, cluster__project=project)
        for item in beneficiary:
            if answers:
                if not item.location:
                    pnt = Point(float(answers[0]), float(answers[1]))
                    item.location = pnt
                    item.save()

    beneficiaries = Beneficiary.objects.filter(~Q(location=None), cluster__project=project)

    data = serialize('custom_geojson', beneficiaries, fields=('name', 'Type', 'location'))
    return HttpResponse(data)


# it contains tabular data of each beneficiary and their progress
class Dashboard2View(LoginRequiredMixin, MultipleObjectMixin, TemplateView):
    template_name = 'core/dashboard-2.html'

    def get(self, request):
        project = self.request.project
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

        beneficiaries = get_beneficiaries(districts, munis, clusters, b_types, project)

        ag = ActivityGroup.objects.filter(project=project).prefetch_related('activity')


        
        page = request.GET.get('page', 1)
        paginator = Paginator(beneficiaries, 100)
        
        try:
            beneficiaries = paginator.page(page)
        except PageNotAnInteger:
            beneficiaries = paginator.page(1)
        except EmptyPage:
            beneficiaries = paginator.page(paginator.num_pages)

        districts = District.objects.filter(id__in=Beneficiary.objects.values('district__id').distinct())
        municipalities = Municipality.objects.filter(id__in=Beneficiary.objects.values('municipality__id').distinct())
        cluster = Cluster.objects.filter(project=project)
        types = Beneficiary.objects.filter(cluster__project=project).values('Type').distinct('Type')
        return render(request, self.template_name, {
            'activity_groups': ag, 
            'beneficiaries': beneficiaries, 
            'districts': districts, 
            'municipalities': municipalities,
            'clusters': cluster,
            'types': types
        })


class BeneficiaryProgressView(LoginRequiredMixin, MultipleObjectMixin, TemplateView):
    template_name = 'core/beneficiary-progress.html'

    def get(self, request):
        beneficiaries = Beneficiary.objects.filter(cluster__project=self.request.project)
        page = request.GET.get('page', 1)
        paginator = Paginator(beneficiaries, 100)
        
        try:
            beneficiaries = paginator.page(page)
        except PageNotAnInteger:
            beneficiaries = paginator.page(1)
        except EmptyPage:
            beneficiaries = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'beneficiaries': beneficiaries})


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

    def get_queryset(self, *args, **kwargs):
        if self.request.is_super_admin:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(project=self.request.project)


class OutputDetailView(ManagerMixin, DetailView):
    model = Output
    template_name = 'core/output-detail.html'


class OutputCreateView(ManagerMixin, CreateView):
    model = Output
    template_name = 'core/output-form.html'
    form_class = OutputForm
    success_url = reverse_lazy('output_list')

    def get_form_kwargs(self):
        kwargs = super(OutputCreateView, self).get_form_kwargs()
        kwargs['project'] = self.request.project
        kwargs['is_super_admin'] = self.request.is_super_admin
        return kwargs


class OutputUpdateView(ManagerMixin, UpdateView):
    model = Output
    template_name = 'core/output-form.html'
    form_class = OutputForm
    success_url = reverse_lazy('output_list')

    def get_form_kwargs(self):
        kwargs = super(OutputUpdateView, self).get_form_kwargs()
        kwargs['project'] = self.request.project
        kwargs['is_super_admin'] = self.request.is_super_admin
        return kwargs


class OutputDeleteView(ManagerMixin, DeleteView):
    model = Output
    template_name = 'core/output-delete.html'
    success_url = reverse_lazy('output_list')


class ActivityGroupListVeiw(ManagerMixin, ListView):
    model = ActivityGroup
    template_name = 'core/activitygroup-list.html'

    def get_queryset(self, *args, **kwargs):
        if self.request.is_super_admin:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(project=self.request.project)


class ActivityGroupDeleteView(ManagerMixin, DeleteView):
    model = ActivityGroup
    template_name = 'core/activitygroup-delete.html'
    success_url = reverse_lazy('activitygroup_list')


class ActivityGroupCreateView(ManagerMixin, CreateView):
    model = ActivityGroup
    template_name = 'core/activitygroup-form.html'
    form_class = ActivityGroupForm
    success_url = reverse_lazy('activitygroup_list')

    def get_form_kwargs(self):
        kwargs = super(ActivityGroupCreateView, self).get_form_kwargs()
        kwargs['project'] = self.request.project
        kwargs['is_super_admin'] = self.request.is_super_admin
        return kwargs


class ActivityGroupUpdateView(ManagerMixin, UpdateView):
    model = ActivityGroup
    template_name = 'core/activitygroup-form.html'
    form_class = ActivityGroupForm
    success_url = reverse_lazy('activitygroup_list')

    def get_form_kwargs(self):
        kwargs = super(ActivityGroupUpdateView, self).get_form_kwargs()
        kwargs['project'] = self.request.project
        kwargs['is_super_admin'] = self.request.is_super_admin
        return kwargs


class ActivityGroupDetailView(ManagerMixin, DetailView):
    model = ActivityGroup
    template_name = 'core/activitygroup-detail.html'


class ActivityListView(ManagerMixin, ListView):
    model = Activity
    template_name = 'core/activity-list.html'

    def get_queryset(self, *args, **kwargs):
        if self.request.is_super_admin:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(activity_group__project=self.request.project)


class ActivityCreateView(ManagerMixin, CreateView):
    model = Activity
    template_name = 'core/activity-form.html'
    form_class = ActivityForm
    success_url = reverse_lazy('activity_list')

    def get_form_kwargs(self):
        kwargs = super(ActivityCreateView, self).get_form_kwargs()
        kwargs['project'] = self.request.project
        kwargs['is_super_admin'] = self.request.is_super_admin
        return kwargs


class ActivityDetailView(ManagerMixin, DetailView):
    model = Activity
    template_name = 'core/activity-detail.html'


class ActivityUpdateView(ManagerMixin, UpdateView):
    model = Activity
    template_name = 'core/activity-form.html'
    form_class = ActivityForm
    success_url = reverse_lazy('activity_list')

    def get_form_kwargs(self):
        kwargs = super(ActivityUpdateView, self).get_form_kwargs()
        kwargs['project'] = self.request.project
        kwargs['is_super_admin'] = self.request.is_super_admin
        return kwargs
        

class ActivityDeleteView(ManagerMixin, DeleteView):
    model = Activity
    template_name = 'core/activity-delete.html'
    success_url = reverse_lazy('activity_list')


class ClusterListView(ManagerMixin, ListView):
    model = Cluster
    template_name = 'core/cluster-list.html'
    context_object_name = 'clusters'

    def get_queryset(self, *args, **kwargs):
        if self.request.is_super_admin:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(project=self.request.project)


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

    def get_form_kwargs(self):
        kwargs = super(ClusterCreateView, self).get_form_kwargs()
        kwargs['project'] = self.request.project
        kwargs['is_super_admin'] = self.request.is_super_admin
        return kwargs


class ClusterDetailView(LoginRequiredMixin, DetailView):
    model = Cluster
    template_name = 'core/cluster-detail.html'


class ClusterUpdateView(ManagerMixin, UpdateView):
    model = Cluster
    template_name = 'core/cluster-form.html'
    form_class = ClusterForm
    success_url = reverse_lazy('cluster_list')

    def get_form_kwargs(self):
        kwargs = super(ClusterUpdateView, self).get_form_kwargs()
        kwargs['project'] = self.request.project
        kwargs['is_super_admin'] = self.request.is_super_admin
        return kwargs


class ClusterDeleteView(ManagerMixin, DeleteView):
    model = Cluster
    template_name = 'core/cluster-delete.html'
    success_url = reverse_lazy('cluster_list')


# for assigning activity groups and activities to clusters
class ClusterAssignView(ManagerMixin, View):

    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        clusterag = ClusterAG.objects.filter(cluster_id=pk, cluster__project=self.request.project).order_by('id')
        activity_group = ActivityGroup.objects.filter(~Q(clusterag__in=clusterag), project=self.request.project).order_by('id')
        selected_activity_group = ClusterAG.objects.filter(cluster_id=pk).select_related('activity_group').order_by('id')
        time_interval = ProjectTimeInterval.objects.filter(project=self.request.project)
        return render(request, 'core/cluster-assign.html',
                      {
                          'activity_group': activity_group,
                          'pk': pk,
                          'selected_activity_group': selected_activity_group,
                          'interval': time_interval
                      })

    @transaction.atomic
    def post(self, request, **kwargs):
        # ag_ represents the activity groups that were selected
        # a_ represents the activities that were selected
        cluster = Cluster.objects.get(pk=kwargs.get('pk'))
        checked = [(name, value) for name, value in request.POST.iteritems()]

        # make sure all the cluster activity groups are deleted before hand assigning activity groups to the cluster
        # this helps to delete the activity groups that were not selected to be assigned if they are already assigned

        ClusterAG.objects.filter(cluster=cluster).delete()

        # for all the selected items
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
                    # is activity is not of beneficiary level then target number and target input are required
                    if not ca.activity.beneficiary_level:
                        for check in checked:
                            # if the cluster activity is already created, any changes are to be recorded in the history
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

    def get_queryset(self, *args, **kwargs):
        if self.request.is_super_admin:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(cluster__project=self.request.project)


class BeneficiaryCreateView(ManagerMixin, CreateView):
    model = Beneficiary
    template_name = 'core/beneficiary-form.html'
    form_class = BeneficiaryForm
    success_url = reverse_lazy('beneficiary_list')

    def get_form_kwargs(self):
        kwargs = super(BeneficiaryCreateView, self).get_form_kwargs()
        kwargs['project'] = self.request.project
        kwargs['is_super_admin'] = self.request.is_super_admin
        return kwargs


class BeneficiaryDetailView(ManagerMixin, DetailView):
    model = Beneficiary
    template_name = 'core/beneficiary-detail.html'


class BeneficiaryUpdateView(ManagerMixin, UpdateView):
    model = Beneficiary
    template_name = 'core/beneficiary-form.html'
    form_class = BeneficiaryForm
    success_url = reverse_lazy('beneficiary_list')

    def get_form_kwargs(self):
        kwargs = super(BeneficiaryUpdateView, self).get_form_kwargs()
        kwargs['project'] = self.request.project
        kwargs['is_super_admin'] = self.request.is_super_admin
        return kwargs


class BeneficiaryDeleteView(ManagerMixin, DeleteView):
    model = Beneficiary
    template_name = 'core/beneficiary-delete.html'
    success_url = reverse_lazy('beneficiary_list')


# change this view if new excel sheets are to be uploaded
# better try matching the headers in the excel sheet
class BeneficiaryUploadView(ManagerMixin, View):
    template_name = 'core/beneficiary-upload.html'

    def post(self, request):
        try:
            filename = request.FILES['inputFile']
            df = pd.read_excel(filename).fillna(value='')
            total = df['Name '].count()
            for row in range(0, total):
                if 'Project' in df:
                    project = Project.objects.get(id=df['Project'][row])
                else:
                    project = Project.objects.last()

                district, created = District.objects.get_or_create(name=df['District '][row])
                municipality, created = Municipality.objects.get_or_create(
                    district=district, name=df['Municipal'][row])
                cluster, created = Cluster.objects.get_or_create(
                    name=df['Cluster'][row],
                    project=project)
                Beneficiary.objects.create(
                    name=df['Name '][row],
                    ward_no=df['Ward'][row],
                    cluster=cluster,
                    Type=df['Category'][row],
                    vulnerabilityType=df['Vulnerability Type'][row],
                    GovernmentTranch=df['Government Tranch Received'][row],
                    ConstructionPhase=df['House Construction Progress (as per 15 steps)'][row],
                    Typesofhouse=df['House Type (CSEB, Brick, Stone)'][row],
                    district=district,
                    municipality=municipality
                )
                # Beneficiary.objects.filter(name=df['Name'][row]).update(district=district, municipality=municipality)
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

    def get_queryset(self, *args, **kwargs):
        if self.request.is_super_admin:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(project=self.request.project)


# class UserRoleCreateView(ManagerMixin, CreateView):
#     model = UserRole
#     template_name = 'core/userrole-form.html'
#     form_class = UserRoleForm
#     success_url = reverse_lazy('userrole_list')


class UserRoleCreateView(ManagerMixin, View):
    def get(self, request, **kwargs):
        form = UserRoleForm(project=self.request.project, is_super_admin=self.request.is_super_admin)
        return render(request, 'core/userrole-form.html', {'form': form})

    def post(self, request, **kwargs):
        form = UserRoleForm(request.POST, project=self.request.project, is_super_admin=self.request.is_super_admin)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            if obj.group.name == 'project-manager':
                clusters = Cluster.objects.filter(project=obj.project)
                for cluster in clusters:
                    obj.cluster.add(cluster)
            else:
                clusters = form.cleaned_data.get('cluster')
                for cluster in clusters:
                    obj.cluster.add(cluster)

            # send email to the user
            if obj.user.email:
                clusters = obj.cluster.all()
                to_email = obj.user.email
                mail_subject = 'User role assigned.'
                message = render_to_string('core/user_role_email.html', {
                    'userrole': obj,
                    'clusters': clusters,
                    'domain': settings.SITE_URL,
                })
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
            else:
                pass
            return HttpResponseRedirect(reverse('userrole_list'))
        return render(request, 'core/userrole-form.html', {'form':form})


class UserRoleUpdateView(ManagerMixin, UpdateView):
    model = UserRole
    template_name = 'core/userrole-form.html'
    form_class = UserRoleForm
    success_url = reverse_lazy('userrole_list')

    def get_form_kwargs(self):
        kwargs = super(UserRoleUpdateView, self).get_form_kwargs()
        kwargs['project'] = self.request.project
        kwargs['is_super_admin'] = self.request.is_super_admin
        return kwargs


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

    def post(self, request, **kwargs):
        aggregations_list = ActivityAggregate.objects.filter(project=self.request.project)
        if 'approve' in request.POST:
            if ',' in request.POST.get('approve'):
                sub_id = request.POST.get('approve').replace(',', '')
            else:
                sub_id = request.POST.get('approve')
            submission = Submission.objects.get(pk=sub_id)
            submission.status = 'approved'
            submission.save()
            
            created = create_db_table(submission)
            if aggregations_list:
                for aggregations in aggregations_list:
                    aggregation_questions = aggregations.aggregation_fields
                    aggregation_answer = aggregations.aggregation_fields_value
                    answer_dict = {}
                    

                    if aggregation_answer == {}:
                        for item in aggregation_questions:
                            for name, attributes in item.items():
                                for key, value in attributes.items():
                                    if key in submission.instance.json:
                                        answer_dict[value] = submission.instance.json[key]
                        aggregations.aggregation_fields_value = answer_dict
                        aggregations.save()
                    else:
                        for item in aggregation_questions:
                            for name, attributes in item.items():
                                for key, value in attributes.items():
                                    if key in submission.instance.json:
                                        if value in aggregation_answer:
                                            previous_answer = aggregation_answer.get(value, '0')
                                            aggregation_answer[value] = str(int(submission.instance.json[key]) + int(previous_answer))
                                        else:
                                            aggregation_answer[value] = submission.instance.json[key]
                        ActivityAggregateHistory.objects.create(aggregation=aggregations, aggregation_values=aggregations.aggregation_fields_value, date=datetime.now())
                        aggregations.aggregation_fields_value = aggregation_answer
                        aggregations.save()


            order = submission.cluster_activity.activity.order
            if order:
                Submission.objects.filter(cluster_activity__activity__order__lte=order, beneficiary__cluster__project=self.request.project).update(status='approved')

        elif 'reject' in request.POST:
            if ',' in request.POST.get('reject'):
                sub_id = request.POST.get('reject').replace(',', '')
            else:
                sub_id = request.POST.get('reject')
            submission = Submission.objects.get(pk=sub_id)
            submission.status = 'rejected'
            submission.save()
            if submission.instance.user:
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

        elif 'approve-all' in request.POST:
            Submission.objects.filter(beneficiary__cluster__project=self.request.project, status='pending').update(status='approved')
            submissions = Submission.objects.filter(beneficiary__cluster__project=self.request.project, status="approved")

            if aggregations_list:
                for aggregations in aggregations_list:
                    aggregation_questions = aggregations.aggregation_fields
                    aggregation_answer = aggregations.aggregation_fields_value
                    answer_dict = {}
                    

                    if aggregation_answer == {}:
                        for item in aggregation_questions:
                            for name, attributes in item.items():
                                for key, value in attributes.items():
                                    for instance in submissions:
                                        if key in instance.instance.json:
                                            answer_dict[value] = instance.instance.json[key]
                        aggregations.aggregation_fields_value = answer_dict
                        aggregations.save()
                    else:
                        for item in aggregation_questions:
                            for name, attributes in item.items():
                                for key, value in attributes.items():
                                    for instance in submissions:
                                        if key in instance.instance.json:
                                            if value in aggregation_answer:
                                                previous_answer = aggregation_answer.get(value, '0')
                                                aggregation_answer[value] = str(int(instance.instance.json[key]) + int(previous_answer))
                                            else:
                                                aggregation_answer[value] = submission.instance.json[key]
                        ActivityAggregateHistory.objects.create(aggregation=aggregations, aggregation_values=aggregations.aggregation_fields_value, date=datetime.now())
                        aggregations.aggregation_fields_value = aggregation_answer
                        aggregations.save()
        
        elif 'approve-selected' in request.POST:
            checked = request.POST.getlist('checked[]')
            if checked:
                for item in checked:
                    submission = Submission.objects.get(id=int(item))
                    submission.status = 'approved'
                    submission.save()
                    created = create_db_table(submission)
                    
                    if aggregations_list:
                        for aggregations in aggregations_list:
                            aggregation_questions = aggregations.aggregation_fields
                            aggregation_answer = aggregations.aggregation_fields_value
                            answer_dict = {}
                            

                            if aggregation_answer == {}:
                                for item in aggregation_questions:
                                    for name, attributes in item.items():
                                        for key, value in attributes.items():
                                            if key in submission.instance.json:
                                                answer_dict[value] = submission.instance.json[key]
                                aggregations.aggregation_fields_value = answer_dict
                                aggregations.save()
                            else:
                                for item in aggregation_questions:
                                    for name, attributes in item.items():
                                        for key, value in attributes.items():
                                            if key in submission.instance.json:
                                                if value in aggregation_answer:
                                                    previous_answer = aggregation_answer.get(value, '0')
                                                    aggregation_answer[value] = str(int(submission.instance.json[key]) + int(previous_answer))
                                                else:
                                                    aggregation_answer[value] = submission.instance.json[key]
                                ActivityAggregateHistory.objects.create(aggregation=aggregations, aggregation_values=aggregations.aggregation_fields_value, date=datetime.now())
                                aggregations.aggregation_fields_value = aggregation_answer
                                aggregations.save()

                    order = submission.cluster_activity.activity.order
                    if order:
                        Submission.objects.filter(beneficiary__cluster__project=self.request.project, cluster_activity__activity__order__lte=order).update(status='approved')
                        # submissions = Submission.objects.filter(cluster_activity__activity__order__lte=order, status="approved").exclude(id=submission.id)

                        # if aggregations_list:
                        #     for aggregations in aggregations_list:
                        #         aggregation_questions = aggregations.aggregation_fields
                        #         aggregation_answer = aggregations.aggregation_fields_value
                        #         answer_dict = {}
                                
                        #         if aggregation_answer == {}:
                        #             for item in aggregation_questions:
                        #                 for name, attributes in item.items():
                        #                     for key, value in attributes.items():
                        #                         for instance in submissions:
                        #                             if key in instance.instance.json:
                        #                                 answer_dict[value] = instance.instance.json[key]
                        #             aggregations.aggregation_fields_value = answer_dict
                        #             aggregations.save()
                        #         else:
                        #             for item in aggregation_questions:
                        #                 for name, attributes in item.items():
                        #                     for key, value in attributes.items():
                        #                         for instance in submissions:
                        #                             if key in instance.instance.json:
                        #                                 if value in aggregation_answer:
                        #                                     previous_answer = aggregation_answer.get(value, '0')
                        #                                     aggregation_answer[value] = str(int(instance.instance.json[key]) + int(previous_answer))
                        #                                 else:
                        #                                     aggregation_answer[value] = submission.instance.json[key]
                        #             ActivityAggregateHistory.objects.create(aggregation=aggregations, aggregation_values=aggregations.aggregation_fields_value, date=datetime.now())
                        #             aggregations.aggregation_fields_value = aggregation_answer
                        #             aggregations.save()
        cluster_activity = ClusterA.objects.get(pk=kwargs.get('pk'))
        submissions = Submission.objects.filter(cluster_activity=cluster_activity)
        return render(request, 'core/submission_list.html', {'submissions': submissions, 'activity': cluster_activity})


class SubNotificationListView(LoginRequiredMixin, View):

    def get(self, request, **kwargs):
        submissions = Submission.objects.filter(status='pending', beneficiary__cluster__project=self.request.project).order_by('instance__date_created')
        page = request.GET.get('page', 1)
        paginator = Paginator(submissions, 200)
        
        try:
            submissions = paginator.page(page)
        except PageNotAnInteger:
            submissions = paginator.page(1)
        except EmptyPage:
            submissions = paginator.page(paginator.num_pages)
        return render(request, 'core/submission_notification.html', {'submissions': submissions})

    def post(self, request, **kwargs):
        aggregations_list = ActivityAggregate.objects.filter(project=self.request.project)
        if 'approve' in request.POST:
            if ',' in request.POST.get('approve'):
                sub_id = request.POST.get('approve').replace(',', '')
            else:
                sub_id = request.POST.get('approve')
            submission = Submission.objects.get(pk=sub_id)
            submission.status = 'approved'
            submission.save()
            created = create_db_table(submission)

            if aggregations_list:
                for aggregations in aggregations_list:
                    aggregation_questions = aggregations.aggregation_fields
                    aggregation_answer = aggregations.aggregation_fields_value
                    answer_dict = {}

                    if aggregation_answer == {}:
                        for item in aggregation_questions:
                            for name, attributes in item.items():
                                for key, value in attributes.items():
                                    if key in submission.instance.json:
                                        answer_dict[value] = submission.instance.json[key]
                        aggregations.aggregation_fields_value = answer_dict
                        aggregations.save()
                    else:
                        for item in aggregation_questions:
                            for name, attributes in item.items():
                                for key, value in attributes.items():
                                    if key in submission.instance.json:
                                        if value in aggregation_answer:
                                            previous_answer = aggregation_answer.get(value, '0')
                                            aggregation_answer[value] = str(int(submission.instance.json[key]) + int(previous_answer))
                                        else:
                                            aggregation_answer[value] = submission.instance.json[key]
                        ActivityAggregateHistory.objects.create(aggregation=aggregations, aggregation_values=aggregations.aggregation_fields_value, date=datetime.now())
                        aggregations.aggregation_fields_value = aggregation_answer
                        aggregations.save()

            order = submission.cluster_activity.activity.order
            if order:
                Submission.objects.filter(cluster_activity__activity__order__lte=order, cluster_activity__activity__activity_group__project=self.request.project).update(status='approved')
                # submissions = Submission.objects.filter(cluster_activity__activity__order__lte=order, status="approved").exclude(id=submission.id)

                # if aggregations_list:
                #     for aggregations in aggregations_list:
                #         aggregation_questions = aggregations.aggregation_fields
                #         aggregation_answer = aggregations.aggregation_fields_value
                #         answer_dict = {}

                #         if aggregation_answer == {}:
                #             for item in aggregation_questions:
                #                 for name, attributes in item.items():
                #                     for key, value in attributes.items():
                #                         for instance in submissions:
                #                             if key in instance.instance.json:
                #                                 answer_dict[value] = instance.instance.json[key]
                #             aggregations.aggregation_fields_value = answer_dict
                #             aggregations.save()
                #         else:
                #             for item in aggregation_questions:
                #                 for name, attributes in item.items():
                #                     for key, value in attributes.items():
                #                         for instance in submissions:
                #                             if key in instance.instance.json:
                #                                 if value in aggregation_answer:
                #                                     previous_answer = aggregation_answer.get(value, '0')
                #                                     aggregation_answer[value] = str(int(instance.instance.json[key]) + int(previous_answer))
                #                                 else:
                #                                     aggregation_answer[value] = submission.instance.json[key]
                #             ActivityAggregateHistory.objects.create(aggregation=aggregations, aggregation_values=aggregations.aggregation_fields_value, date=datetime.now())
                #             aggregations.aggregation_fields_value = aggregation_answer
                #             aggregations.save()

        elif 'reject' in request.POST:

            if ',' in request.POST.get('reject'):
                sub_id = request.POST.get('reject').replace(',', '')
            else:
                sub_id = request.POST.get('reject')
            submission = Submission.objects.get(pk=sub_id)
            submission.status = 'rejected'
            submission.save()
            if submission.instance.user:
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
        elif 'approve-all' in request.POST:
            Submission.objects.filter(beneficiary__cluster__project=self.request.project, status='pending').update(status='approved')
            submissions = Submission.objects.filter(beneficiary__cluster__project=self.request.project, status="approved")

            if aggregations_list:
                for aggregations in aggregations_list:
                    aggregation_questions = aggregations.aggregation_fields
                    aggregation_answer = aggregations.aggregation_fields_value
                    answer_dict = {}

                    if aggregation_answer == {}:
                        for item in aggregation_questions:
                            for name, attributes in item.items():
                                for key, value in attributes.items():
                                    for instance in submissions:
                                        if key in instance.instance.json:
                                            answer_dict[value] = instance.instance.json[key]
                        aggregations.aggregation_fields_value = answer_dict
                        aggregations.save()
                    else:
                        for item in aggregation_questions:
                            for name, attributes in item.items():
                                for key, value in attributes.items():
                                    for instance in submissions:
                                        if key in instance.instance.json:
                                            if value in aggregation_answer:
                                                previous_answer = aggregation_answer.get(value, '0')
                                                aggregation_answer[value] = str(int(instance.instance.json[key]) + int(previous_answer))
                                            else:
                                                aggregation_answer[value] = submission.instance.json[key]
                        ActivityAggregateHistory.objects.create(aggregation=aggregations, aggregation_values=aggregations.aggregation_fields_value, date=datetime.now())
                        aggregations.aggregation_fields_value = aggregation_answer
                        aggregations.save()
        
        elif 'approve-selected' in request.POST:
            checked = request.POST.getlist('checked[]')
            if checked:
                for item in checked:
                    submission = Submission.objects.get(id=int(item))
                    submission.status = 'approved'
                    submission.save()
                    created = create_db_table(submission)

                    if aggregations_list:
                        for aggregations in aggregations_list:
                            aggregation_questions = aggregations.aggregation_fields
                            aggregation_answer = aggregations.aggregation_fields_value
                            answer_dict = {}
                            
                            if aggregation_answer == {}:
                                for item in aggregation_questions:
                                    for name, attributes in item.items():
                                        for key, value in attributes.items():
                                            if key in submission.instance.json:
                                                answer_dict[value] = submission.instance.json[key]
                                aggregations.aggregation_fields_value = answer_dict
                                aggregations.save()
                            else:
                                for item in aggregation_questions:
                                    for name, attributes in item.items():
                                        for key, value in attributes.items():
                                            if key in submission.instance.json:
                                                if value in aggregation_answer:
                                                    previous_answer = aggregation_answer.get(value, '0')
                                                    aggregation_answer[value] = str(int(submission.instance.json[key]) + int(previous_answer))
                                                else:
                                                    aggregation_answer[value] = submission.instance.json[key]
                                ActivityAggregateHistory.objects.create(aggregation=aggregations, aggregation_values=aggregations.aggregation_fields_value, date=datetime.now())
                                aggregations.aggregation_fields_value = aggregation_answer
                                aggregations.save()

                    order = submission.cluster_activity.activity.order
                    if order:
                        Submission.objects.filter(cluster_activity__activity__order__lte=order, cluster_activity__activity__activity_group__project=self.request.project).update(status='approved')
                        # submissions = Submission.objects.filter(cluster_activity__activity__order__lte=order, status="approved").exclude(id=submission.id)

                        # if aggregations_list:
                        #     for aggregations in aggregations_list:
                        #         aggregation_questions = aggregations.aggregation_fields
                        #         aggregation_answer = aggregations.aggregation_fields_value
                        #         answer_dict = {}

                        #         if aggregation_answer == {}:
                        #             for item in aggregation_questions:
                        #                 for name, attributes in item.items():
                        #                     for key, value in attributes.items():
                        #                         for instance in submissions:
                        #                             if key in instance.instance.json:
                        #                                 answer_dict[value] = instance.instance.json[key]
                        #             aggregations.aggregation_fields_value = answer_dict
                        #             aggregations.save()
                        #         else:
                        #             for item in aggregation_questions:
                        #                 for name, attributes in item.items():
                        #                     for key, value in attributes.items():
                        #                         for instance in submissions:
                        #                             if key in instance.instance.json:
                        #                                 if value in aggregation_answer:
                        #                                     previous_answer = aggregation_answer.get(value, '0')
                        #                                     aggregation_answer[value] = str(int(instance.instance.json[key]) + int(previous_answer))
                        #                                 else:
                        #                                     aggregation_answer[value] = submission.instance.json[key]
                        #             ActivityAggregateHistory.objects.create(aggregation=aggregations, aggregation_values=aggregations.aggregation_fields_value, date=datetime.now())
                        #             aggregations.aggregation_fields_value = aggregation_answer
                        #             aggregations.save()

        submissions = Submission.objects.filter(status='pending').order_by('instance__date_created')
        page = request.GET.get('page', 1)
        paginator = Paginator(submissions, 200)
        
        try:
            submissions = paginator.page(page)
        except PageNotAnInteger:
            submissions = paginator.page(1)
        except EmptyPage:
            submissions = paginator.page(paginator.num_pages)
        return render(request, 'core/submission_notification.html', {'submissions': submissions})

class ConfigUpdateView(UpdateView):
    model = Config
    template_name = 'core/config-form.html'
    form_class = ConfigForm

    def get_success_url(self):
        return reverse('config_edit', kwargs={'pk': 1})

# update the target number from the submission listing page
@transaction.atomic
def update_cluster_activity(request, **kwargs):
    pk = kwargs.get('pk')
    ca = ClusterA.objects.get(pk=pk)
    target_number = request.POST.get('target_number')
    cahistory = ClusterAHistory()
    if target_number is not None:
        if not ca.target_completed == float(target_number):
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
        elif role.group.name == 'project-management-unit':
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
            clusters = Cluster.objects.filter(municipality__id__in=municipalities, project=request.project).distinct()
            clusters = serialize("json", clusters)
            return HttpResponse(clusters)
        else:
            clusters = Cluster.objects.filter(project=request.project)
            clusters = serialize("json", clusters)
            return HttpResponse(clusters)
    else:
        return HttpResponse('not ajax request')


def get_activity_group(request):
    if request.is_ajax():
        clusters = request.GET.getlist('clusters[]')
        if clusters:
            cluster_activity_groups = ClusterAG.objects.filter(cluster_id__in=clusters)
            if cluster_activity_groups:
                cluster_activity_groups_list = []
                for item in cluster_activity_groups:
                    cluster_activity_groups_list.append(item.activity_group.id)
                activity_groups = ActivityGroup.objects.filter(id__in=cluster_activity_groups_list)
                activity_groups = serialize("json", activity_groups)
                return HttpResponse(activity_groups)
            else:
                activity_groups = ActivityGroup.objects.filter(project=request.project)
                activity_groups = serialize("json", activity_groups)
                return HttpResponse(activity_groups)
        else:
            activity_groups = ActivityGroup.objects.filter(project=request.project)
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
            activity = Activity.objects.filter(activity_group__project=request.project)
            activity = serialize("json", activity)
            return HttpResponse(activity)
    else:
        return HttpResponse('not ajax request')


class ActivityAssignListView(ManagerMixin, ListView):
    model = Activity
    template_name = 'core/activity-assign-list.html'

    def get_queryset(self, *args, **kwargs):
        if self.request.is_super_admin:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(activity_group__project=self.request.project)


def assign_activity(request, *args, **kwargs):
    activity = Activity.objects.get(pk=kwargs.get('pk'))
    if request.method == 'GET':
        cluster_activity = ClusterA.objects.filter(activity=activity)
        clusters = Cluster.objects.filter(~Q(clusterag__ca__activity=activity), project=request.project)

    elif request.method == 'POST':
        activity = Activity.objects.get(pk=kwargs.get('pk'))
        cluster_activity = ClusterA.objects.filter(activity=activity)
        clusters = Cluster.objects.filter(~Q(clusterag__ca__activity=activity), project=request.project)
        if 'assign' in request.POST:
            cluster = request.POST.getlist('clusters[]')
            for item in cluster:
                cluster = Cluster.objects.get(id=int(item))
                cag = ClusterAG.objects.create(cluster=cluster, activity_group=activity.activity_group)
                ca, created = ClusterA.objects.get_or_create(
                    activity=activity,
                    cag=cag,
                )

                if activity.beneficiary_level:
                    ca.target_number = None
                    ca.target_unit = None
                    ca.location = None
                
                else:
                    ca.target_number = activity.target_number
                    ca.target_unit = activity.target_unit
                    if activity.location:
                        ca.location = activity.location
                ca.time_interval = activity.time_interval
                ca.save()
                        
    return render(request, 'core/activity-assign.html', {'clusters': clusters})


def edit_submission(request,  id_string, data_id):
    context = RequestContext(request)
    xform = get_object_or_404(
        XForm, id_string__exact=id_string)
    instance = get_object_or_404(
        Instance, pk=data_id, xform=xform)
    form = instance.xform
    # if not has_change_form_permission(request, form, 'edit'):
    #     raise PermissionDenied


    instance_attachments = image_urls_dict(instance)
    # check permission
    # if not has_edit_permission(xform, owner, request, xform.shared):
    #     return HttpResponseForbidden(_(u'Not shared.'))
    if not hasattr(settings, 'ENKETO_URL'):
        response = render_to_response('base.html', {},
                                      context_instance=RequestContext(request))
        response.status_code = 500
        return response

    injected_xml = inject_instanceid(instance.xml, instance.uuid)

    form_url = _get_form_url(request, xform.user.username, settings.ENKETO_PROTOCOL)

    try:
        url = enketo_url(
            form_url, xform.id_string, instance_xml=injected_xml,
            instance_id=instance.uuid, return_url="",
            instance_attachments=instance_attachments
        )
    except Exception as e:
        context.message = {
            'type': 'alert-error',
            'text': u"Enketo error, reason: %s" % e}
        messages.add_message(
            request, messages.WARNING,
            _("Enketo error: enketo replied %s") % e, fail_silently=True)
    else:
        if url:
            context.enketo = url
            return HttpResponseRedirect(url)

    response = render_to_response('base.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

def get_progress(request):
    types = Beneficiary.objects.filter(cluster__project=request.project).values('Type').distinct()
    progress_data = []
    categories = []
    project=request.project
    
    for item in types:
        total_list = []
        beneficiary = Beneficiary.objects.filter(Type=item['Type'], cluster__project=project)
        beneficiary_progress = 0
        for obj in beneficiary:
            beneficiary_progress += obj.progress
        try:
            total_list.append(round(beneficiary_progress / len(beneficiary), 2))
        except Exception:
            total_list.append(beneficiary_progress/1)
        if not total_list == [0.0]:
            progress_data.append(total_list)
            categories.append(item['Type'])
    
    data = {'categories': categories, 'progress_data': progress_data}
    return JsonResponse(data)
    # progress_data = {}
    # if clusters:
    #     # for cluster progress bar data
    #     # gives the data of the volume of beneficiaries that have completed all the activities as per the type of beneficiaries
    #     # increase by 1 if all the activities have been completed(all submissions are approved)
        
    #     selected_clusters = Cluster.objects.filter(id__in=clusters).order_by('name')
    #     for item in types:
    #         total_list = []
    #         for obj in selected_clusters:
    #             beneficiary = Beneficiary.objects.filter(cluster=obj, Type=item['Type'])
    #             beneficiary_progress = 0
    #             for obj in beneficiary:
    #                 if Submission.objects.filter(beneficiary=obj).exists():
    #                     submissions = Submission.objects.filter(beneficiary=obj, status='approved').values(
    #                         'beneficiary__Type'). \
    #                         annotate(progress=Sum('cluster_activity__activity__weight'))
    #                     for submission in submissions:
    #                         beneficiary_progress += submission['progress']
    #                 else:
    #                     pass
    #             try:
    #                 total_list.append(round(beneficiary_progress / len(beneficiary), 2))
    #             except Exception:
    #                 total_list.append(beneficiary_progress/1)
    #         progress_data[str(item['Type'])] = total_list
    #     for item in selected_clusters:
    #         categories.append(str(item.name))
        
    #     data = {'categories': categories, 'progress_data': progress_data}
    #     return JsonResponse(data)
    
    # elif munis:
    #     selected_munis = Municipality.objects.filter(id__in=munis).order_by('name')
    #     clusters = Cluster.objects.filter(municipality__in=selected_munis)
    #     for item in types:
    #         total_list = []
    #         for obj in selected_munis:
    #             beneficiary = Beneficiary.objects.filter(municipality=obj, Type=item['Type'])
    #             beneficiary_progress = 0
    #             for obj in beneficiary:
    #                 if Submission.objects.filter(beneficiary=obj).exists():
    #                     submissions = Submission.objects.filter(beneficiary=obj, status='approved').values(
    #                         'beneficiary__Type'). \
    #                         annotate(progress=Sum('cluster_activity__activity__weight'))
    #                     for submission in submissions:
    #                         beneficiary_progress += submission['progress']
    #                 else:
    #                     pass
    #             try:
    #                 total_list.append(round(beneficiary_progress / len(beneficiary), 2))
    #             except Exception:
    #                 total_list.append(beneficiary_progress / 1)
    #         progress_data[str(item['Type'])] = total_list
    #     for item in selected_munis:
    #         categories.append(str(item.name))
        
    #     data = {'categories': categories, 'progress_data': progress_data}
    #     return JsonResponse(data)
    
    # elif select_districts:
    #     selected_districts = District.objects.filter(id__in=districts).order_by('name')
    #     clusters = Cluster.objects.filter(municipality__district__in=selected_districts)
    #     for item in types:
    #         total_list = []
    #         for obj in selected_districts:
    #             beneficiary = Beneficiary.objects.filter(district=obj, Type=item['Type'])
    #             beneficiary_progress = 0
    #             for obj in beneficiary:
    #                 if Submission.objects.filter(beneficiary=obj).exists():
    #                     submissions = Submission.objects.filter(beneficiary=obj, status='approved').values(
    #                         'beneficiary__Type'). \
    #                         annotate(progress=Sum('cluster_activity__activity__weight'))
    #                     for submission in submissions:
    #                         beneficiary_progress += submission['progress']
    #                 else:
    #                     pass
    #             try:
    #                 total_list.append(round(beneficiary_progress / len(beneficiary), 2))
    #             except Exception:
    #                 total_list.append(beneficiary_progress / 1)
    #         progress_data[str(item['Type'])] = total_list
    #     for item in selected_districts:
    #         categories.append(str(item.name))
        
    #     data = {'categories': categories, 'progress_data': progress_data}
    #     return JsonResponse(data)
    
    # else:
    #     selected_districts = District.objects.filter(id__in=Beneficiary.objects.filter(cluster__project=request.project).values('district__id').distinct())
    #     for item in types:
    #         total_list = []
    #         for obj in selected_districts:
    #             beneficiary = Beneficiary.objects.filter(district=obj, Type=item['Type'])
    #             beneficiary_progress = 0
    #             for obj in beneficiary:
    #                 if Submission.objects.filter(beneficiary=obj).exists():
    #                     submissions = Submission.objects.filter(beneficiary=obj, status='approved').values('beneficiary__Type').\
    #                         annotate(progress=Sum('cluster_activity__activity__weight'))
    #                     for submission in submissions:
    #                         beneficiary_progress += submission['progress']
    #                 else:
    #                     pass
    #             try:
    #                 total_list.append(round(beneficiary_progress / len(beneficiary), 2))
    #             except Exception:
    #                 total_list.append(beneficiary_progress / 1)
    #         progress_data[str(item['Type'])] = total_list
    #     for item in selected_districts:
    #         categories.append(str(item.name))
        
    #     data = {'categories': categories, 'progress_data': progress_data}
    #     return JsonResponse(data)


def get_progress_phase_pie(request):
    project = request.project
    types = Beneficiary.objects.filter(cluster__project=project).values('Type').distinct()
    construction_phases = {}

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

    if clusters:
        activity_groups = ActivityGroup.objects.filter(project=project, output__name='House Construction')
        construction_phases = {}
        for ag in activity_groups:
            beneficiaries = 0
            phases = []
            activities = Activity.objects.filter(activity_group=ag)
            beneficiary = Beneficiary.objects.filter(
                submissions__cluster_activity__cag__cluster__in=clusters,
                submissions__cluster_activity__cag__activity_group=ag,
            )
            for item in beneficiary:
                completed = True
                for activity in activities:
                    submission = Submission.objects.filter(beneficiary=item, cluster_activity__activity=activity)
                    for s in submission:
                        if s.status != 'approved':
                            completed = False
                if completed:
                    beneficiaries += 1
            beneficiary = [round((float(beneficiaries) / len(activity_groups)) * 100, 2)]
            phases.append(beneficiary)
            construction_phases[str(ag.name)] = phases

        data = {'data': construction_phases}
        return JsonResponse(data)
    
    elif munis:
        activity_groups = ActivityGroup.objects.filter(project=project, output__name='House Construction')
        construction_phases = {}
        for ag in activity_groups:
            beneficiaries = 0
            phases = []
            activities = Activity.objects.filter(activity_group=ag)
            beneficiary = Beneficiary.objects.filter(
                submissions__cluster_activity__cag__cluster__in=clusters,
                submissions__cluster_activity__cag__activity_group=ag,
            )
            for item in beneficiary:
                completed = True
                for activity in activities:
                    submission = Submission.objects.filter(beneficiary=item, cluster_activity__activity=activity)
                    for s in submission:
                        if s.status != 'approved':
                            completed = False
                if completed:
                    beneficiaries += 1
            beneficiary = [round((float(beneficiaries) / len(activity_groups)) * 100, 2)]
            phases.append(beneficiary)
            construction_phases[str(ag.name)] = phases
        
        data = {'data': construction_phases}
        return JsonResponse(data)
    
    elif select_districts:
        activity_groups = ActivityGroup.objects.filter(project=project, output__name='House Construction')
        construction_phases = {}
        for ag in activity_groups:
            beneficiaries = 0
            phases = []
            activities = Activity.objects.filter(activity_group=ag)
            beneficiary = Beneficiary.objects.filter(
                submissions__cluster_activity__cag__cluster__in=clusters,
                submissions__cluster_activity__cag__activity_group=ag,
            )
            for item in beneficiary:
                completed = True
                for activity in activities:
                    submission = Submission.objects.filter(beneficiary=item, cluster_activity__activity=activity)
                    for s in submission:
                        if s.status != 'approved':
                            completed = False
                if completed:
                    beneficiaries += 1
            beneficiary = [round((float(beneficiaries) / len(activity_groups)) * 100, 2)]
            phases.append(beneficiary)
            construction_phases[str(ag.name)] = phases
        
        data = {'data': construction_phases}
        return JsonResponse(data)
    
    else:
        clusters = Cluster.objects.filter(project=request.project).order_by('name')
        activity_groups = ActivityGroup.objects.filter(project=project, output__name='House Construction')
        construction_phases = {}
        for ag in activity_groups:
            beneficiaries = 0
            phases = []
            activities = Activity.objects.filter(activity_group=ag)
            beneficiary = Beneficiary.objects.filter(
                submissions__cluster_activity__cag__cluster__in=clusters,
                submissions__cluster_activity__cag__activity_group=ag,
            )
            for item in beneficiary:
                completed = True
                for activity in activities:
                    submission = Submission.objects.filter(beneficiary=item, cluster_activity__activity=activity)
                    for s in submission:
                        if s.status != 'approved':
                            completed = False
                if completed:
                    beneficiaries += 1
            beneficiary = [round((float(beneficiaries) / len(activity_groups)) * 100, 2)]
            phases.append(beneficiary)
            construction_phases[str(ag.name)] = phases
        data = {'data': construction_phases}
        return JsonResponse(data)
    

class MapDasboardView(ManagerMixin, TemplateView):
    template_name = 'core/map_dashboard.html'


from .get_question_answer import get_questions

def get_aggregation_fields(request, *args, **kwargs):
    question_json = XForm.objects.get(id=request.GET.get('form_id', 0)).json
    questions = []
    questions = get_questions(question_json)
    return JsonResponse(questions, safe=False)


def aggregation_settings(request, *args, **kwargs):
    if request.method == 'GET':
        forms = XForm.objects.all()
        add_forms = list(XForm.objects.all().values('id', 'title'))
        add_forms = json.dumps(add_forms)
        return render(request, 'core/aggregation-settings.html', {'forms': forms, 'add_forms': add_forms})
    
    if request.method == "POST":
        aggregation_fields = []
        aggregation_field_main_dict = {}
        for i in range(1, 10):
            form_name = str(i) + '-act-form'
            if form_name in request.POST: 
                form_id = request.POST.get(form_name)
                if form_id in request.POST:
                    aggregation_fields_dict = {}
                    for field in request.POST.getlist(form_id):
                        field_question , field_label = field.split('|')
                        aggregation_fields_dict[field_question] = field_label
                    id_string = XForm.objects.get(id=form_id).id_string
                    aggregation_field_main_dict[id_string] = aggregation_fields_dict
            else:
                break
        aggregation_fields.append(aggregation_field_main_dict)

        if len(aggregation_fields) > 0:
            aggregation_name = request.POST.get('aggregation_label', '')
            if ActivityAggregate.objects.filter(name=aggregation_name, project=request.project).exists():
                act_aggregate = ActivityAggregate.objects.get(name=aggregation_name, project=request.project)
                act_aggregate.aggregation_fields = aggregation_fields
                act_aggregate.save()
            else:
                ActivityAggregate.objects.create(name=aggregation_name, aggregation_fields=aggregation_fields, project=request.project)
            
        return HttpResponseRedirect('/core/aggregation-list')


class AggregateView(ManagerMixin, TemplateView):
    template_name = 'core/aggregation-view.html'

    def get(self, request, *args, **kwargs):
        try:
            aggregations = ActivityAggregate.objects.filter(project=self.request.project)
            for aggregate in aggregations:
                aggregate_question = aggregate.aggregation_fields
                aggregation_answer = aggregate.aggregation_fields_value
                if aggregation_answer == {}:
                    answer_dict = {}
                    submissions = Submission.objects.filter(status='approved', cluster_activity__activity__activity_group__project=request.project)
                    for sub in submissions:
                        for item in aggregate_question:
                            for name, attributes in item.items():
                                if name in sub.instance.json['_xform_id_string']:
                                    for key, value in attributes.items():
                                        if key in sub.instance.json:
                                            previous_answer = answer_dict.get(value, '0')
                                            new_answer = int(previous_answer) + int(sub.instance.json[key])
                                            answer_dict[value] = str(new_answer)
                    aggregate.aggregation_fields_value = answer_dict
                    aggregate.save()

        except Exception as e:
            print('exception occured', e)
            aggregations = {}
        return render(request, self.template_name, {'aggregations': aggregations})

class AggregationListView(ManagerMixin, TemplateView):
    template_name = 'core/aggregation-list.html'

    def get(self, request, *args, **kwargs):
        aggregations = ActivityAggregate.objects.filter(project=request.project)
        return render(request, self.template_name, {'aggregations': aggregations})


class AggregationDeleteView(ManagerMixin, DeleteView):
    model = ActivityAggregate
    template_name = 'core/aggregation-delete.html'
    success_url = reverse_lazy('aggregation-list')


class AggregationEditView(ManagerMixin, TemplateView):
    template_name = 'core/aggregation-edit.html'

    def get(self, request, *args, **kwargs):
        forms = XForm.objects.all()
        aggregation = ActivityAggregate.objects.get(pk=self.kwargs.get('pk'))
        aggregation_fields = aggregation.aggregation_fields
        aggregation_fields = json.dumps(aggregation_fields)
        add_forms = list(XForm.objects.all().values('id', 'title'))
        add_forms = json.dumps(add_forms)
        return render(request, self.template_name, {'forms': forms, 'aggregation': aggregation, 'aggregation_fields': aggregation_fields, 'add_forms': add_forms})

    def post(self, request, *args, **kwargs):
        aggregation_fields = []
        aggregation_field_main_dict = {}
        for i in range(1, 10):
            form_name = str(i) + '-act-form'
            if form_name in request.POST: 
                form_id = request.POST.get(form_name)
                if form_id in request.POST:
                    aggregation_fields_dict = {}
                    for field in request.POST.getlist(form_id):
                        field_question , field_label = field.split('|')
                        aggregation_fields_dict[field_question] = field_label
                    print(aggregation_fields_dict)
                    id_string = XForm.objects.get(id=form_id).id_string
                    aggregation_field_main_dict[id_string] = aggregation_fields_dict
            else:
                break
        aggregation_fields.append(aggregation_field_main_dict)

        if len(aggregation_fields) > 0:
            aggregation_name = request.POST.get('aggregation_label', '')
            act_aggregate = ActivityAggregate.objects.get(id=self.kwargs.get('pk'))
            act_aggregate.aggregation_fields = aggregation_fields
            act_aggregate.name = aggregation_name
            act_aggregate.save()

            ActivityAggregateHistory.objects.create(aggregation=act_aggregate, aggregation_values=act_aggregate.aggregation_fields_value, date=datetime.now())
        return HttpResponseRedirect('/core/aggregation-list')
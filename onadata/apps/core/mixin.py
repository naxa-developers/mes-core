from functools import wraps
from django.views.generic.edit import UpdateView as BaseUpdateView, CreateView as BaseCreateView, \
    DeleteView as BaseDeleteView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from onadata.apps.core.models import Project
from onadata.apps.core.models import UserRole


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)


class ProjectRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.project:
            raise PermissionDenied()
        return super(ProjectRequiredMixin, self).dispatch(request, *args, **kwargs)


class SuperAdminMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not UserRole.objects.filter(user=request.user, group__name="super-admin"):
            raise PermissionDenied()
        return super(SuperAdminMixin, self).dispatch(request, *args, **kwargs)


class DeleteView(BaseDeleteView):
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = super(DeleteView, self).post(request, *args, **kwargs)
        messages.success(request, ('%s %s' % (self.object.__class__._meta.verbose_name.title(), _('successfully deleted!'))))
        return response

class UpdateView(BaseUpdateView):
    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['scenario'] = _('Edit')
        context['base_template'] = 'core/base.html'
        super(UpdateView, self).get_context_data()
        return context


class CreateView(BaseCreateView):
    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['scenario'] = _('Add')
        base_template = 'core/base.html'
        context['base_template'] = base_template
        return context


class ProjectView(LoginRequiredMixin):
    def form_valid(self, form):
        if self.request.project:
            form.instance.project = self.request.project
        return super(ProjectView, self).form_valid(form)

    def get_queryset(self):
        if self.request.project:
            return super(ProjectView, self).get_queryset().filter(project=self.request.project)
        return []

    def get_form(self, *args, **kwargs):
        form = super(ProjectView, self).get_form(*args, **kwargs)
        if self.request.project:
            form.project = self.request.project
        if hasattr(form.Meta, 'project_filters'):
            for field in form.Meta.project_filters:
                if self.request.project:
                    form.fields[field].queryset = Project.objects.filter(id=self.request.project.pk)
        return form


USER_PERMS = {
    'mobilizer': ['community-social-mobilizer', 'social-mobilizer', 'super-admin'],
    'project': ['project-management-unit', 'project-coordinator', 'project-manager', 'super-admin'],
    'manager_only': ['project-manager', 'project-management-unit'],
    'manager': ['project-manager', 'super-admin', 'project-management-unit'],
    'admin': ['super-admin'],
    'normal': ['social-mobilizer', 'project-coordinator'],
    'donor': ['donor']
}

class ProjectMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.role.group.name in USER_PERMS['project']:
                return super(ProjectMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()

class ManagerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.role.group.name in USER_PERMS['manager']:
                return super(ManagerMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class AdminMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.role.group.name in USER_PERMS['admin']:
                return super(AdminMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class CommunitySocialMobilizerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.role.group.name == 'community-social-mobilizer':
                return super(CommunitySocialMobilizerMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class SocialMobilizerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.role.group.name == 'social-mobilizer':
                return super(SocialMobilizerMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()

# use in all view functions
def group_required(group_name):
    def _check_group(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated():
                if request.role.group.name in USER_PERMS.get(group_name, []):
                    return view_func(request, *args, **kwargs)
            raise PermissionDenied()

        return wrapper

    return _check_group
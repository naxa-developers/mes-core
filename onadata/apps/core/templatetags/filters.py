# -*- coding: utf-8 -*-

import importlib
from django.template import Library
from django import template
from django.contrib.auth.models import Group
from onadata.apps.core.mixin import USER_PERMS
from onadata.apps.core.models import Submission, ClusterA, UserRole, ClusterAHistory, Cluster, Activity, ClusterAG
from django.db.models import Q

register = Library()

@register.tag
def ifrole(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, role = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires exactly two arguments" % token.contents.split()[0]
        )
    if not (role[0] == role[-1] and role[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name
        )
    nodelist = parser.parse('endrole', )
    parser.delete_first_token()
    return RoleInGroup(role[1:-1], nodelist)


class RoleInGroup(template.Node):
    def __init__(self, role, nodelist):
        self.role = role
        self.nodelist = nodelist

    def render(self, context):
        request = template.resolve_variable('request', context)
        try:
            if UserRole.objects.filter(project__id=request.session.get('project_id', 0), user=request.user).exists():
                roles = UserRole.objects.filter(project__id=request.session.get('project_id', 0), user=request.user)
                role = roles[0]
            if role and role.group.name in USER_PERMS[self.role]:
                return self.nodelist.render(context)
            else:
                return ''
        except:
            if request.role and request.role.group.name in USER_PERMS[self.role]:
                return self.nodelist.render(context)
            else:
                return ''


class GroupCheckNode(template.Node):
    def __init__(self, groups, nodelist_true, nodelist_false):
        self.groups = groups
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def render(self, context):
        user = template.resolve_variable('user', context)

        if not user.is_authenticated():
            return self.nodelist_false.render(context)

        allowed = False
        for checkgroup in self.groups:

            if checkgroup.startswith('"') and checkgroup.endswith('"'):
                checkgroup = checkgroup[1:-1]

            if checkgroup.startswith("'") and checkgroup.endswith("'"):
                checkgroup = checkgroup[1:-1]

            try:
                group = Group.objects.get(name=checkgroup)
            except Group.DoesNotExist:
                break

            if group in user.groups.all():
                allowed = True
                break

        if allowed:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)


@register.filter
def setting(path):
    to_import = '.'.join(path.split('.')[:-2])
    imported = importlib.import_module(to_import)
    group_name = path.split('.')[-2:-1][0]
    group = getattr(imported, group_name)
    attr_name = path.split('.')[-1]
    val = getattr(group, attr_name)
    return val


@register.filter
def cluster_activity_submission_count(obj):
    return Submission.objects.filter(cluster_activity=obj).count()


@register.filter
def cluster_activity_group_submission_count(obj):
    ca = ClusterA.objects.filter(cag=obj)
    count = 0
    for item in ca:
        count += Submission.objects.filter(cluster_activity=item).count()
    return count


@register.filter
def check_cluster_activity(obj, cag):
    if ClusterA.objects.filter(activity=obj, cag=cag).exists():
        return True
    else:
        return False


@register.filter
def get_cluster_activity(obj, cag):
    if ClusterA.objects.filter(activity=obj, cag=cag).exists():
        return ClusterA.objects.get(activity=obj, cag=cag)
    else:
        return obj


@register.filter
def get_cluster_name(pk):
    return Cluster.objects.get(pk=pk).name


@register.filter
def get_ca_history(obj, cag=None):
    if cag is not None:
        if ClusterA.objects.filter(activity=obj, cag=cag).exists():
            ca = ClusterA.objects.filter(activity=obj, cag=cag)
            return ClusterAHistory.objects.filter(clustera=ca)

    else:
        return ClusterAHistory.objects.filter(clustera=obj)


@register.filter
def check_manager_permission(obj, cluster):
    project = cluster.project
    try:
        user_role = UserRole.objects.get(Q(user=obj), Q(cluster=cluster), project=project)
    except:
        user_role = UserRole.objects.get(user=obj, project=project)

    if user_role.group.name in ['project-manager', 'super-admin']:
        return True
    else:
        return False


@register.filter
def check_status_change_permission(obj, request):
    current_user_role = UserRole.objects.filter(user=request.user)
    user = obj.instance.user
    submitted_user_role = UserRole.objects.filter(user=user)
    if current_user_role[0].group.name == 'social-mobilizer' and submitted_user_role[0].group.name == 'community-social-mobilizer':
        return True
    elif current_user_role[0].group.name == 'project-coordinator' and submitted_user_role[0].group.name == 'social-mobilizer':
        return True
    elif current_user_role[0].group.name in ['project-manager', 'project-management-unit', 'super-admin']:
        return True
    else:
        return False


@register.filter
def get_activity_count(obj):
    return Activity.objects.filter(~Q(weight=0), activity_group=obj).count()


@register.filter
def check_activity_progress(obj, beneficiary=None):
    try:
        higher_activities = Activity.objects.filter(order__gte=obj.order, activity_group__project=obj.activity_group.project)
        if higher_activities:
            for item in higher_activities:
                cag = ClusterAG.objects.filter(cluster=beneficiary.cluster, activity_group=item.activity_group)
                ca = ClusterA.objects.filter(activity=item, cag__in=cag)
                if beneficiary is not None:
                    if Submission.objects.filter(cluster_activity__in=ca, beneficiary=beneficiary, status="approved").exists():
                        return True

                else:
                    if Submission.objects.filter(cluster_activity__in=ca, status="approved").exists():
                        return True
        cag = ClusterAG.objects.filter(cluster=beneficiary.cluster, activity_group=obj.activity_group)
        ca = ClusterA.objects.filter(activity=obj, cag__in=cag)
        if beneficiary is not None:
            if Submission.objects.filter(cluster_activity__in=ca, beneficiary=beneficiary, status="approved").exists():
                return True

        else:
            if Submission.objects.filter(cluster_activity__in=ca, status="approved").exists():
                return True
        return False
    except:
        return False


@register.filter
def get_beneficiary_progress(obj):
    submission = Submission.objects.filter(beneficiary=obj)
    progress = 0
    for item in submission:
        if item.status == 'approved':
            progress += item.cluster_activity.activity.weight
    return progress


@register.filter
def get_project_manager(obj):
    userrole = UserRole.objects.get(project=obj, group__name="project-manager")
    return userrole.user.username


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.

    It also removes any empty parameters to keep things neat,
    so you can remove a parm by setting it to ``""``.

    For example, if you're on the page ``/things/?with_frosting=true&page=5``,
    then

    <a href="/things/?{% param_replace page=3 %}">Page 3</a>

    would expand to

    <a href="/things/?with_frosting=true&page=3">Page 3</a>

    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()

@register.filter
def get_range(obj):
    return range(1, obj+1)


@register.filter
def abbreviate(obj):
    splits = obj.split(' ')
    abbr = []
    for item in splits:
        if item not in ['and', 'with', 'of', 'the', 'a', 'for', 'an', 'in', 'as', 'by', 'into']:
            abbr.append(item[0])
    return abbr

@register.filter
def get_answer(obj, aggregation):
    if obj in aggregation.aggregation_fields_value:
        return aggregation.aggregation_fields_value[obj]
    else:
        return 0

@register.filter
def get_sum(aggregation):
    obj = aggregation.aggregation_fields[0]
    sum = 0
    if obj == {}:
        return sum
    else:
        for key, value in obj.items():
            for question, answer in value.items():
                if answer in aggregation.aggregation_fields_value:
                    sum += int(aggregation.aggregation_fields_value[answer])
    return sum
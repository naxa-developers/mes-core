# -*- coding: utf-8 -*-

import importlib
from django.template import Library
from django import template
from django.contrib.auth.models import Group
from onadata.apps.core.mixin import USER_PERMS

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

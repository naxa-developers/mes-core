from onadata.apps.core.models import Project, UserRole, ActivityGroup, Activity

def userroleprocessor(request):
    if request.user.is_authenticated():
        user = request.user 
        if 'project_id' in request.session:
            project = Project.objects.get(id=request.session.get('project_id'))
        else:
            project = request.project

        return {'role': UserRole.objects.get(user=user, project=project)}
    else:
        return {}


def baseprocessor(request):
    if 'project_id' in request.session:
        project = Project.objects.get(id=request.session.get('project_id'))
    else:
        project = request.project
    dynamic_beneficiaries = ActivityGroup.objects.filter(activity__is_registration=True, project=project)
    return {'dynamic_beneficiaries': dynamic_beneficiaries}
from onadata.apps.core.models import Project, UserRole, ActivityGroup, Activity

def userroleprocessor(request):
    if request.user.is_authenticated():
        user = request.user 
        if 'project_id' in request.session:
            project = Project.objects.get(id=request.session.get('project_id'))
        else:
            project = request.project
        
        try:
            role = UserRole.objects.get(user=user, project=project)
        except:
            role = UserRole.objects.filter(user=user)[0]

        return {'role': role}
    else:
        return {}


def baseprocessor(request):
    if 'project_id' in request.session:
        project = Project.objects.get(id=request.session.get('project_id'))
    else:
        project = request.project
    dynamic_beneficiaries = ActivityGroup.objects.filter(activity__is_registration=True, project=project)
    return {'dynamic_beneficiaries': dynamic_beneficiaries}
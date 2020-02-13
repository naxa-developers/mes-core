from onadata.apps.core.models import Project, UserRole

def userroleprocessor(request):
    user = request.user
    project = Project.objects.get(id=request.session.get('project_id'))

    return {'role': UserRole.objects.get(user=user, project=project)}
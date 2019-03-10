from django.contrib import admin

from onadata.apps.core.models import Project, Output, ActivityGroup, Activity, Cluster, Beneficiary

admin.site.register(Project)
admin.site.register(Output)
admin.site.register(ActivityGroup)
admin.site.register(Activity)
admin.site.register(Cluster)
admin.site.register(Beneficiary)

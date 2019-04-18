from django.contrib import admin

from onadata.apps.core.models import Project, Output, ActivityGroup, Activity, Cluster, Beneficiary, UserRole,\
    ClusterAG, ClusterA, Config, District, Municipality

admin.site.register(Project)
admin.site.register(Output)
admin.site.register(ActivityGroup)
admin.site.register(Activity)
admin.site.register(Cluster)
admin.site.register(Beneficiary)
admin.site.register(UserRole)
admin.site.register(ClusterAG)
admin.site.register(ClusterA)
admin.site.register(Config)
admin.site.register(District)
admin.site.register(Municipality)

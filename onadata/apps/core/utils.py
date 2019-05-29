from datetime import datetime
from django.core.serializers import serialize


# divide a datetime range into intervals
def get_interval(start, end, interval):
    start = str(start).split('+')[0]
    end = str(end).split('+')[0]
    start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    duration = end.year - start.year
    if not duration == 0:
        interval = interval * duration
    # gives the interval in which the ranges are to be separated
    diff = (end - start) / interval
    ranges = []
    # get the intervals except the end date
    for i in range(interval):
        ranges.append(start + diff * i)
    # append the end date to the list
    ranges.append(end)
    return ranges


def get_clusters(districts=None, munis=None, clusters=None):
    from .models import Cluster
    if clusters and munis and districts:
        muni_cluster = Cluster.objects.filter(municipality__in=munis)
        for item in muni_cluster:
            clusters.append(item.id)

        district_cluster = Cluster.objects.filter(municipality__district__in=districts)
        for item in district_cluster:
            clusters.append(item.id)

        clust = Cluster.objects.filter(id__in=clusters).order_by('name')

    elif clusters:
        clust = Cluster.objects.filter(id__in=clusters).order_by('name')

    elif munis:
        muni_cluster = Cluster.objects.filter(municipality__in=munis)
        for item in muni_cluster:
            clusters.append(item.id)

        clust = Cluster.objects.filter(id__in=clusters).order_by('name')

    elif districts:
        district_cluster = Cluster.objects.filter(municipality__district__in=districts)
        for item in district_cluster:
            clusters.append(item.id)

        clust = Cluster.objects.filter(id__in=clusters).order_by('name')

    else:
        clust = Cluster.objects.order_by('name')

    return clust


# get the beneficiary list on the basis of filters applied
def get_beneficiaries(districts=None, munis=None, clusters=None, b_types=None):
    from .models import Cluster, Beneficiary
    if clusters and b_types and munis and districts:
        muni_cluster = Cluster.objects.filter(municipality__in=munis)
        for item in muni_cluster:
            clusters.append(item.id)

        district_cluster = Cluster.objects.filter(municipality__district__in=districts)
        for item in district_cluster:
            clusters.append(item.id)

        beneficiaries = Beneficiary.objects.filter(cluster__in=clusters, Type__in=b_types).order_by('name')

    elif b_types:
        beneficiaries = Beneficiary.objects.filter(Type__in=b_types).order_by('name')

    elif clusters:
        beneficiaries = Beneficiary.objects.filter(cluster__in=clusters).order_by('name')

    elif munis:
        muni_cluster = Cluster.objects.filter(municipality__in=munis)
        for item in muni_cluster:
            clusters.append(item.id)

        beneficiaries = Beneficiary.objects.filter(cluster__in=clusters).order_by('name')

    elif districts:
        district_cluster = Cluster.objects.filter(municipality__district__in=districts)
        for item in district_cluster:
            clusters.append(item.id)

        beneficiaries = Beneficiary.objects.filter(cluster__in=clusters).order_by('name')

    else:
        beneficiaries = Beneficiary.objects.order_by('name')

    return beneficiaries


def get_cluster_activity_data(project, activity=None):
    from onadata.apps.core.models import ClusterA, ProjectTimeInterval, ClusterAHistory

    bar_data = {}
    interval_target_number = []
    interval_achievement = []
    time_intervals = ProjectTimeInterval.objects.filter(project=project).order_by('label')
    for item in time_intervals:
        tg_num = 0
        completed_tg_num = 0
        if activity:
            if ClusterA.objects.filter(time_interval=item, activity_id__in=activity).exists():
                cluster_activity = ClusterA.objects.filter(time_interval=item, activity_id__in=activity)
                for obj in cluster_activity:
                    if obj.target_number or obj.target_completed:
                        tg_num += obj.target_number
                        completed_tg_num += obj.target_completed
            elif ClusterAHistory.objects.filter(
                    time_interval=item, clustera__activity_id__in=activity).exists():
                cluster_activity_history = ClusterAHistory.objects.filter(
                    time_interval=item, clustera__activity_id__in=activity)
                for obj in cluster_activity_history:
                    if obj.target_number or obj.target_completed:
                        tg_num += obj.target_number
                        completed_tg_num += obj.target_completed

        else:
            if ClusterA.objects.filter(time_interval=item).exists():
                cluster_activity = ClusterA.objects.filter(time_interval=item)
                for obj in cluster_activity:
                    if obj.target_number or obj.target_completed:
                        tg_num += obj.target_number
                        completed_tg_num += obj.target_completed
            elif ClusterAHistory.objects.filter(time_interval=item).exists():
                cluster_activity_history = ClusterAHistory.objects.filter(time_interval=item)
                for obj in cluster_activity_history:
                    if obj.target_number or obj.target_completed:
                        tg_num += obj.target_number
                        completed_tg_num += obj.target_completed
        interval_target_number.append(tg_num)
        interval_achievement.append(completed_tg_num)
    bar_data['Target Number'] = interval_target_number
    bar_data['Achievement'] = interval_achievement

    return bar_data


def get_progress_data(project, types=None, clusters=None, districts=None, munis=None):
    from .models import District, Municipality, Cluster, Submission, ProjectTimeInterval, ClusterA, Activity, \
        ActivityGroup, ClusterAG, Beneficiary
    from django.db.models import Sum, Count

    progress_data = {}
    cluster_progress_data = {}
    categories = []
    map_data = []
    if clusters:

        # for cluster progress bar data
        selected_clusters = Cluster.objects.filter(id__in=clusters).order_by('name')
        for item in types:
            total_list = []
            for obj in selected_clusters:
                if Submission.objects.filter(
                        cluster_activity__cag__cluster_id=obj.id,
                        status='approved',
                        beneficiary__Type=item['Type']).exists():
                    submissions = Submission.objects.filter(
                        cluster_activity__cag__cluster_id=obj.id, status='approved',
                        beneficiary__Type=item['Type']
                    ).values('beneficiary__Type').distinct().annotate(
                        progress=Sum('cluster_activity__activity__weight'), beneficiary_count=Count('beneficiary__Type'))
                    for submission in submissions:
                        total_list.append((submission['progress'] / submission['beneficiary_count']) * 100)
                else:
                    total_list.append(0)
            progress_data[str(item['Type'])] = total_list
        for item in selected_clusters:
            categories.append(str(item.name))

        # for cluster progress line data
        interval = ProjectTimeInterval.objects.filter(project=project).order_by('label')
        for item in selected_clusters:
            total_list = []
            for obj in interval:
                if Submission.objects.filter(cluster_activity__time_interval=obj, status='approved',
                                             cluster_activity__cag__cluster=item).exists():
                    submissions = Submission.objects.filter(
                        cluster_activity__time_interval=obj,
                        status='approved', cluster_activity__cag__cluster=item).\
                        values('cluster_activity').\
                        distinct().annotate(
                        progress=Sum('cluster_activity__activity__weight'))
                    for submission in submissions:
                        total_list.append(submission['progress'])
                elif Submission.objects.filter(
                        clustera_history__time_interval=obj,
                        status='approved', clustera_history__clustera__cag__cluster=item).exists():
                    submissions = Submission.objects.filter(
                        clustera_history__time_interval=obj,
                        status='approved', clustera_history__clustera__cag__cluster=item).\
                        values('clustera_history'). \
                        distinct().annotate(
                        progress=Sum('cluster_activity__activity__weight'))
                    for submission in submissions:
                        total_list.append(submission['progress'])
                else:
                    total_list.append(0)
            cluster_progress_data[str(item.name)] = total_list

        # for cluster phase pie chart
        activity_groups = ActivityGroup.objects.filter(project=project, output__name='House Construction')
        cluster_phases = {}
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
            cluster_phases[str(ag.name)] = phases

        return progress_data, categories, cluster_progress_data, cluster_phases

    elif munis:
        selected_munis = Municipality.objects.filter(id__in=munis).order_by('name')
        for item in types:
            total_list = []
            for obj in selected_munis:
                clusters = obj.cluster.all().order_by('name')
                if Submission.objects.filter(
                        cluster_activity__cag__cluster__in=clusters,
                        status='approved',
                        beneficiary__Type=item['Type']).exists():
                    submissions = Submission.objects.filter(
                        cluster_activity__cag__cluster__in=clusters, status='approved',
                        beneficiary__Type=item['Type']
                    ).values('beneficiary__Type').distinct().annotate(
                        progress=Sum('cluster_activity__activity__weight'), beneficiary_count=Count('beneficiary__Type'))
                    for submission in submissions:
                        total_list.append((submission['progress'] / submission['beneficiary_count']) * 100)
                else:
                    total_list.append(0)
            progress_data[str(item['Type'])] = total_list
        for item in selected_munis:
            categories.append(str(item.name))

        interval = ProjectTimeInterval.objects.filter(project=project).order_by('label')
        for item in clusters:
            total_list = []
            for obj in interval:
                if Submission.objects.filter(cluster_activity__time_interval=obj, status='approved',
                                             cluster_activity__cag__cluster=item).exists():
                    submissions = Submission.objects.filter(
                        cluster_activity__time_interval=obj,
                        status='approved', cluster_activity__cag__cluster=item).\
                        values('cluster_activity'). \
                        distinct().annotate(
                        progress=Sum('cluster_activity__activity__weight'))
                    for submission in submissions:
                        total_list.append(submission['progress'])
                elif Submission.objects.filter(
                        clustera_history__time_interval=obj,
                        status='approved', clustera_history__clustera__cag__cluster=item).exists():
                    submissions = Submission.objects.filter(
                        clustera_history__time_interval=obj,
                        status='approved', clustera_history__clustera__cag__cluster=item).\
                        values('clustera_history'). \
                        distinct().annotate(
                        progress=Sum('cluster_activity__activity__weight'))
                    for submission in submissions:
                        total_list.append(submission['progress'])
                else:
                    total_list.append(0)
            cluster_progress_data[str(item.name)] = total_list

        # for cluster phase pie chart
        activity_groups = ActivityGroup.objects.filter(project=project, output__name='House Construction')
        cluster_phases = {}
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
            cluster_phases[str(ag.name)] = phases

        return progress_data, categories, cluster_progress_data, cluster_phases

    elif districts:
        selected_districts = District.objects.filter(id__in=districts).order_by('name')
        for item in types:
            total_list = []
            for obj in selected_districts:
                municipality = Municipality.objects.filter(district=obj).order_by('name')
                clusters = Cluster.objects.filter(municipality__in=municipality).order_by('name')
                if Submission.objects.filter(
                        cluster_activity__cag__cluster__in=clusters,
                        status='approved',
                        beneficiary__Type=item['Type']).exists():
                    submissions = Submission.objects.filter(
                        cluster_activity__cag__cluster__in=clusters, status='approved',
                        beneficiary__Type=item['Type']
                    ).values('beneficiary__Type').distinct().annotate(
                        progress=Sum('cluster_activity__activity__weight'), beneficiary_count=Count('beneficiary__Type'))
                    for submission in submissions:
                        total_list.append((submission['progress'] / submission['beneficiary_count']) * 100)
                else:
                    total_list.append(0)
            progress_data[str(item['Type'])] = total_list
        for item in selected_districts:
            categories.append(str(item.name))

        interval = ProjectTimeInterval.objects.filter(project=project).order_by('label')
        for item in clusters:
            total_list = []
            for obj in interval:
                if Submission.objects.filter(cluster_activity__time_interval=obj, status='approved',
                                             cluster_activity__cag__cluster=item).exists():
                    submissions = Submission.objects.filter(
                        cluster_activity__time_interval=obj,
                        status='approved', cluster_activity__cag__cluster=item).\
                        values('cluster_activity'). \
                        distinct().annotate(
                        progress=Sum('cluster_activity__activity__weight'))
                    for submission in submissions:
                        total_list.append(submission['progress'])
                elif Submission.objects.filter(
                        clustera_history__time_interval=obj,
                        status='approved', clustera_history__clustera__cag__cluster=item).exists():
                    submissions = Submission.objects.filter(
                        clustera_history__time_interval=obj,
                        status='approved', clustera_history__clustera__cag__cluster=item).\
                        values('clustera_history'). \
                        distinct().annotate(
                        progress=Sum('cluster_activity__activity__weight'))
                    for submission in submissions:
                        total_list.append(submission['progress'])
                else:
                    total_list.append(0)
            cluster_progress_data[str(item.name)] = total_list

        # for cluster phase pie chart
        activity_groups = ActivityGroup.objects.filter(project=project, output__name='House Construction')
        cluster_phases = {}
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
            cluster_phases[str(ag.name)] = phases

        return progress_data, categories, cluster_progress_data, cluster_phases

    else:
        selected_districts = District.objects.all().order_by('name')
        for item in types:
            total_list = []
            for obj in selected_districts:
                municipality = Municipality.objects.filter(district=obj).order_by('name')
                clusters = Cluster.objects.filter(municipality__in=municipality).order_by('name')
                if Submission.objects.filter(
                        cluster_activity__cag__cluster__in=clusters,
                        status='approved',
                        beneficiary__Type=item['Type']).exists():
                    submissions = Submission.objects.filter(
                        cluster_activity__cag__cluster__in=clusters, status='approved',
                        beneficiary__Type=item['Type']
                    ).values('beneficiary__Type').distinct().annotate(
                        progress=Sum('cluster_activity__activity__weight'), beneficiary_count=Count('beneficiary__Type'))
                    for submission in submissions:
                        total_list.append((submission['progress'] / submission['beneficiary_count']) * 100)
                else:
                    total_list.append(0)
            progress_data[str(item['Type'])] = total_list
        for item in selected_districts:
            categories.append(str(item.name))

        interval = ProjectTimeInterval.objects.filter(project=project).order_by('label')
        clusters = Cluster.objects.filter(project=project).order_by('name')
        for item in clusters:
            total_list = []
            for obj in interval:
                if Submission.objects.filter(cluster_activity__time_interval=obj, status='approved', cluster_activity__cag__cluster=item).exists():
                    submissions = Submission.objects.filter(
                        cluster_activity__time_interval=obj,
                        status='approved', cluster_activity__cag__cluster=item).\
                        values('cluster_activity').\
                        distinct().annotate(
                        progress=Sum('cluster_activity__activity__weight'))
                    for submission in submissions:

                        total_list.append(submission['progress'])
                elif Submission.objects.filter(
                        clustera_history__time_interval=obj,
                        status='approved', clustera_history__clustera__cag__cluster=item).exists():
                    submissions = Submission.objects.filter(
                        clustera_history__time_interval=obj,
                        status='approved', clustera_history__clustera__cag__cluster=item).\
                        values('clustera_history'). \
                        distinct().annotate(
                        progress=Sum('cluster_activity__activity__weight'))
                    for submission in submissions:
                        total_list.append(submission['progress'])
                else:
                    total_list.append(0)
            cluster_progress_data[str(item.name)] = total_list

        # for cluster phase pie chart
        activity_groups = ActivityGroup.objects.filter(project=project, output__name='House Construction')
        cluster_phases = {}
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
            cluster_phases[str(ag.name)] = phases

        return progress_data, categories, cluster_progress_data, cluster_phases

from datetime import datetime


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

    elif clusters or munis or districts:
        if clusters:
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

        elif clusters and munis:
            muni_cluster = Cluster.objects.filter(municipality__in=munis)
            for item in muni_cluster:
                clusters.append(item.id)

            clust = Cluster.objects.filter(id__in=clusters).order_by('name')

        elif clusters and districts:
            district_cluster = Cluster.objects.filter(municipality__district__in=districts)
            for item in district_cluster:
                clusters.append(item.id)

            clust = Cluster.objects.filter(id__in=clusters).order_by('name')

        elif clusters and munis and districts:
            muni_cluster = Cluster.objects.filter(municipality__in=munis)
            for item in muni_cluster:
                clusters.append(item.id)

            district_cluster = Cluster.objects.filter(municipality__district__in=districts)
            for item in district_cluster:
                clusters.append(item.id)

            clust = Cluster.objects.filter(id_in=clusters).order_by('name')

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

    elif clusters or b_types or munis or districts:
        if b_types:
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

        elif b_types and clusters:
            beneficiaries = Beneficiary.objects.filter(cluster__in=clusters, Type__in=b_types).order_by('name')

        elif b_types and munis:
            muni_cluster = Cluster.objects.filter(municipality__in=munis)
            for item in muni_cluster:
                clusters.append(item.id)

            beneficiaries = Beneficiary.objects.filter(cluster__in=clusters, Type__in=b_types).order_by('name')

        elif b_types and districts:
            district_cluster = Cluster.objects.filter(municipality__district__in=districts)
            for item in district_cluster:
                clusters.append(item.id)

            beneficiaries = Beneficiary.objects.filter(cluster__in=clusters, Type__in=b_types).order_by('name')

        elif clusters and munis:
            muni_cluster = Cluster.objects.filter(municipality__in=munis)
            for item in muni_cluster:
                clusters.append(item.id)

            beneficiaries = Beneficiary.objects.filter(cluster__in=clusters).order_by('name')

        elif clusters and districts:
            district_cluster = Cluster.objects.filter(municipality__district__in=districts)
            for item in district_cluster:
                clusters.append(item.id)

            beneficiaries = Beneficiary.objects.filter(cluster__in=clusters).order_by('name')

        elif munis and districts:
            muni_cluster = Cluster.objects.filter(municipality__in=munis)
            for item in muni_cluster:
                clusters.append(item.id)

            district_cluster = Cluster.objects.filter(municipality__district__in=districts)
            for item in district_cluster:
                clusters.append(item.id)

            beneficiaries = Beneficiary.objects.filter(cluster__in=clusters).order_by('name')

        elif b_types and clusters and munis:
            muni_cluster = Cluster.objects.filter(municipality__in=munis)
            for item in muni_cluster:
                clusters.append(item.id)

            beneficiaries = Beneficiary.objects.filter(cluster__in=clusters, Type__in=b_types).order_by('name')

        elif b_types and clusters and districts:
            district_cluster = Cluster.objects.filter(municipality__district__in=districts)
            for item in district_cluster:
                clusters.append(item.id)

            beneficiaries = Beneficiary.objects.filter(cluster__in=clusters, Type__in=b_types).order_by('name')

        elif b_types and districts and munis:
            muni_cluster = Cluster.objects.filter(municipality__in=munis)
            for item in muni_cluster:
                clusters.append(item.id)

            district_cluster = Cluster.objects.filter(municipality__district__in=districts)
            for item in district_cluster:
                clusters.append(item.id)

            beneficiaries = Beneficiary.objects.filter(cluster__in=clusters, Type__in=b_types).order_by('name')

        elif clusters and munis and districts:

            muni_cluster = Cluster.objects.filter(municipality__in=munis)
            for item in muni_cluster:
                clusters.append(item.id)

            district_cluster = Cluster.objects.filter(municipality__district__in=districts)
            for item in district_cluster:
                clusters.append(item.id)

            beneficiaries = Beneficiary.objects.filter(cluster__in=clusters).order_by('name')

    else:
        beneficiaries = Beneficiary.objects.order_by('name')

    return beneficiaries


def get_cluster_activity_data(project, activity_group=None, activity=None):
    from onadata.apps.core.models import ClusterA, ProjectTimeInterval, ClusterAHistory

    bar_data = {}
    interval_target_number = []
    interval_achievement = []
    time_intervals = ProjectTimeInterval.objects.filter(project=project).order_by('label')
    for item in time_intervals:
        tg_num = 0
        completed_tg_num = 0
        if activity_group and activity:
            if ClusterA.objects.filter(
                    time_interval=item, activity_id__in=activity, activity__activity_group_id__in=activity_group
            ).exists():
                cluster_activity = ClusterA.objects.filter(
                    time_interval=item, activity_id__in=activity, activity__activity_group_id__in=activity_group)
                for obj in cluster_activity:
                    if obj.target_number or obj.target_completed:
                        tg_num += obj.target_number
                        completed_tg_num += obj.target_completed
            elif ClusterAHistory.objects.filter(
                    time_interval=item,
                    clustera__activity_id__in=activity,
                    clustera__activity__activity_group_id__in=activity_group).exists():
                cluster_activity_history = ClusterAHistory.objects.filter(
                    time_interval=item,
                    clustera__activity_id__in=activity,
                    clustera__activity__activity_group_id__in=activity_group)
                for obj in cluster_activity_history:
                    if obj.target_number or obj.target_completed:
                        tg_num += obj.target_number
                        completed_tg_num += obj.target_completed

        elif activity_group or activity:
            if activity_group:
                if ClusterA.objects.filter(time_interval=item, activity__activity_group_id__in=activity_group).exists():
                    cluster_activity = ClusterA.objects.filter(
                        time_interval=item, activity__activity_group_id__in=activity_group)
                    for obj in cluster_activity:
                        if obj.target_number or obj.target_completed:
                            tg_num += obj.target_number
                            completed_tg_num += obj.target_completed
                elif ClusterAHistory.objects.filter(
                        time_interval=item, clustera__activity__activity_group_id__in=activity_group).exists():
                    cluster_activity_history = ClusterAHistory.objects.filter(
                        time_interval=item, clustera__activity__activity_group_id__in=activity_group)
                    for obj in cluster_activity_history:
                        if obj.target_number or obj.target_completed:
                            tg_num += obj.target_number
                            completed_tg_num += obj.target_completed

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
    from .models import District, Municipality, Cluster, Submission, ProjectTimeInterval
    from django.db.models import Sum

    progress_data = {}
    cluster_progress_data = {}
    categories = []
    if clusters:
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
                        progress=Sum('cluster_activity__activity__weight'))
                    for submission in submissions:
                        total_list.append(submission['progress'])
                else:
                    total_list.append(0)
            progress_data[str(item['Type'])] = total_list
        for item in selected_clusters:
            categories.append(str(item.name))

        interval = ProjectTimeInterval.objects.filter(project=project).order_by('label')
        for item in selected_clusters:
            total_list = []
            for obj in interval:
                if Submission.objects.filter(cluster_activity__time_interval=obj, status='approved',
                                             cluster_activity__cag__cluster=item).exists():
                    submissions = Submission.objects.filter(
                        cluster_activity__time_interval=obj,
                        status='approved', cluster_activity__cag__cluster=item).values('cluster_activity'). \
                        distinct().annotate(progress=Sum('cluster_activity__activity__weight'))
                    for submission in submissions:
                        total_list.append(submission['progress'])
                elif Submission.objects.filter(
                        clustera_history__time_interval=obj,
                        status='approved', clustera_history__clustera__cag__cluster=item).exists():
                    submissions = Submission.objects.filter(
                        clustera_history__time_interval=obj,
                        status='approved', clustera_history__clustera__cag__cluster=item).values('clustera_history'). \
                        distinct().annotate(progress=Sum('cluster_activity__activity__weight'))
                    for submission in submissions:
                        total_list.append(submission['progress'])
                else:
                    total_list.append(0)
            cluster_progress_data[str(item.name)] = total_list

        return progress_data, categories, cluster_progress_data

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
                        progress=Sum('cluster_activity__activity__weight'))
                    for submission in submissions:
                        total_list.append(submission['progress'])
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
                        status='approved', cluster_activity__cag__cluster=item).values('cluster_activity'). \
                        distinct().annotate(progress=Sum('cluster_activity__activity__weight'))
                    for submission in submissions:
                        total_list.append(submission['progress'])
                elif Submission.objects.filter(
                        clustera_history__time_interval=obj,
                        status='approved', clustera_history__clustera__cag__cluster=item).exists():
                    submissions = Submission.objects.filter(
                        clustera_history__time_interval=obj,
                        status='approved', clustera_history__clustera__cag__cluster=item).values('clustera_history'). \
                        distinct().annotate(progress=Sum('cluster_activity__activity__weight'))
                    for submission in submissions:
                        total_list.append(submission['progress'])
                else:
                    total_list.append(0)
            cluster_progress_data[str(item.name)] = total_list

        return progress_data, categories, cluster_progress_data

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
                        progress=Sum('cluster_activity__activity__weight'))
                    for submission in submissions:
                        total_list.append(submission['progress'])
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
                        status='approved', cluster_activity__cag__cluster=item).values('cluster_activity'). \
                        distinct().annotate(progress=Sum('cluster_activity__activity__weight'))
                    for submission in submissions:
                        total_list.append(submission['progress'])
                elif Submission.objects.filter(
                        clustera_history__time_interval=obj,
                        status='approved', clustera_history__clustera__cag__cluster=item).exists():
                    submissions = Submission.objects.filter(
                        clustera_history__time_interval=obj,
                        status='approved', clustera_history__clustera__cag__cluster=item).values('clustera_history'). \
                        distinct().annotate(progress=Sum('cluster_activity__activity__weight'))
                    for submission in submissions:
                        total_list.append(submission['progress'])
                else:
                    total_list.append(0)
            cluster_progress_data[str(item.name)] = total_list

        return progress_data, categories, cluster_progress_data

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
                        progress=Sum('cluster_activity__activity__weight'))
                    for submission in submissions:
                        total_list.append(submission['progress'])
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
                        status='approved', cluster_activity__cag__cluster=item).values('cluster_activity').\
                        distinct().annotate(progress=Sum('cluster_activity__activity__weight'))
                    for submission in submissions:
                        total_list.append(submission['progress'])
                elif Submission.objects.filter(
                        clustera_history__time_interval=obj,
                        status='approved', clustera_history__clustera__cag__cluster=item).exists():
                    submissions = Submission.objects.filter(
                        clustera_history__time_interval=obj,
                        status='approved', clustera_history__clustera__cag__cluster=item).values('clustera_history'). \
                        distinct().annotate(progress=Sum('cluster_activity__activity__weight'))
                    for submission in submissions:
                        total_list.append(submission['progress'])
                else:
                    total_list.append(0)
            cluster_progress_data[str(item.name)] = total_list

        return progress_data, categories, cluster_progress_data

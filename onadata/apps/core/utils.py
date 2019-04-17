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

from rest_framework import serializers

from .models import ActivityGroup, Activity, Output, Project, Cluster, Beneficiary

class ProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Project
		fields = ('name', 'description', 'sector', 'start_date', 'end_date', 'reporting_period', 'beneficiaries')


class ActivitySerializer(serializers.ModelSerializer):
	class Meta:
		model = Activity
		fields = ('activity_group', 'name', 'description', 'target_number', 'target_unit', 'start_date', 'end_date', 'form', 'target_complete', 'beneficiary_level', 'published', 'target_met')

	
class ActivityGroupSerializer(serializers.ModelSerializer):
	activity = ActivitySerializer(many=True, read_only=True)

	class Meta:
		model = ActivityGroup
		fields = ('output', 'name', 'description', 'activity')


class OutputSerializer(serializers.ModelSerializer):
	class Meta:
		model = Output
		fields = ('name', 'description','project')


class ClusterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cluster
		fields = ('name', 'project', 'activity_group', 'district', 'municipality', 'ward')


class BeneficiarySerialzier(serializers.ModelSerializer):
	class Meta:
		model = Beneficiary
		fields = ('identifier', 'name', 'address', 'cluster', 'type_id')
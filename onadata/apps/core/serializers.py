from rest_framework import serializers

from .models import ActivityGroup, Activity, Output, Project, Cluster, Beneficiary



class OutputSerializer(serializers.ModelSerializer):
	class Meta:
		model = Output
		fields = ('id', 'name', 'description','project')


class ProjectSerializer(serializers.ModelSerializer):
	output = OutputSerializer(many=True, read_only=True)

	class Meta:
		model = Project
		fields = ('id', 'name', 'description', 'sector', 'start_date', 'end_date', 'reporting_period', 'beneficiaries', 'output')


class ActivitySerializer(serializers.ModelSerializer):
	id_string = serializers.SerializerMethodField()


	def get_id_string(self, obj):
		if obj.form:
			return obj.form.id_string
		else:
			return None


	class Meta:
		model = Activity
		fields = ('id', 'name', 'description', 'target_number', 'target_unit', 'start_date', 'end_date', 'form', 'id_string', 'target_complete', 'beneficiary_level', 'published', 'target_met')



	
class ActivityGroupSerializer(serializers.ModelSerializer):
	activity = ActivitySerializer(many=True, read_only=True)

	class Meta:
		model = ActivityGroup
		fields = ('id', 'output', 'name', 'description', 'activity', 'cluster')



class BeneficiarySerialzier(serializers.ModelSerializer):
	class Meta:
		model = Beneficiary
		fields = ('id', 'name', 'address', 'ward_no', 'cluster', 'Type')



class ClusterSerializer(serializers.ModelSerializer):
	activitygroup = ActivityGroupSerializer(many=True, read_only=True)

	class Meta:
		model = Cluster
		fields = ('id', 'name', 'district', 'municipality', 'ward', 'activitygroup')


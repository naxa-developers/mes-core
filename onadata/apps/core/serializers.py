from rest_framework import serializers

from .models import ActivityGroup, Activity, Output, Project, Cluster, Beneficiary



class OutputSerializer(serializers.ModelSerializer):
	class Meta:
		model = Output
		fields = ('name', 'description','project')


class ProjectSerializer(serializers.ModelSerializer):
	output = OutputSerializer(many=True, read_only=True)

	class Meta:
		model = Project
		fields = ('name', 'description', 'sector', 'start_date', 'end_date', 'reporting_period', 'beneficiaries', 'output')


class ActivitySerializer(serializers.ModelSerializer):
	id_string = serializers.SerializerMethodField()


	def get_id_string(self, obj):
		if obj.form:
			return obj.form.id_string
		else:
			return ''


	class Meta:
		model = Activity
		fields = ('name', 'description', 'target_number', 'target_unit', 'start_date', 'end_date', 'form', 'id_string', 'target_complete', 'beneficiary_level', 'published', 'target_met')



	
class ActivityGroupSerializer(serializers.ModelSerializer):
	activity = ActivitySerializer(many=True, read_only=True)

	class Meta:
		model = ActivityGroup
		fields = ('output', 'name', 'description', 'activity', 'cluster')



class BeneficiarySerialzier(serializers.ModelSerializer):
	class Meta:
		model = Beneficiary
		fields = ('identifier', 'name', 'address', 'cluster', 'type_id')



class ClusterSerializer(serializers.ModelSerializer):
	# beneficiary = BeneficiarySerialzier(many=True, read_only=True)
	activitygroup = ActivityGroupSerializer(many=True, read_only=True)

	class Meta:
		model = Cluster
		fields = ('name', 'project', 'district', 'municipality', 'ward', 'activitygroup')


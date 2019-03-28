from rest_framework import serializers
from django.db.models import Max

from datetime import datetime
import time

from .models import ActivityGroup, Activity, Output, Project, Cluster, Beneficiary, ClusterAG, ClusterA, Config



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
		fields = ('id', 'name', 'description', 'target_number', 'target_unit', 'start_date', 'end_date', 'form', 'id_string', 'beneficiary_level')



	
class ActivityGroupSerializer(serializers.ModelSerializer):
	activity = ActivitySerializer(many=True, read_only=True)

	class Meta:
		model = ActivityGroup
		fields = ('id', 'output', 'name', 'description', 'activity')



class BeneficiarySerialzier(serializers.ModelSerializer):
	class Meta:
		model = Beneficiary
		fields = ('id', 'name', 'address', 'ward_no', 'cluster', 'Type')



class CASerializer(serializers.ModelSerializer):
	id_string = serializers.SerializerMethodField()


	def get_id_string(self, obj):
		if obj.activity.form:
			return obj.activity.form.id_string
		else:
			return None

	name = serializers.ReadOnlyField(source='activity.name')
	description = serializers.ReadOnlyField(source='activity.description')
	target_number = serializers.ReadOnlyField(source='activity.target_number')
	target_unit = serializers.ReadOnlyField(source='activity.target_unit')
	start_date = serializers.ReadOnlyField(source='activity.start_date')
	end_date = serializers.ReadOnlyField(source='activity.end_date')
	form = serializers.ReadOnlyField(source='activity.form.id')
	beneficiary_level = serializers.ReadOnlyField(source='activity.beneficiary_level')

	class Meta:
		model = ClusterA
		# fields = ('id', 'name', 'description', 'target_number', 'target_unit', 'start_date', 'end_date', 'form', 'id_string', 'beneficiary_level')
		fields = ('id', 'name','description', 'target_number', 'target_unit', 'start_date', 'end_date', 'form', 'id_string', 'beneficiary_level')


class CAGSerializer(serializers.ModelSerializer):
	ca = CASerializer(many=True, read_only=True)
	output = serializers.ReadOnlyField(source='activity_group.output.name')
	name = serializers.ReadOnlyField(source='activity_group.name')
	description = serializers.ReadOnlyField(source='activity_group.description')


	class Meta:
		model = ClusterAG
		fields = ('id', 'output', 'name', 'description', 'ca')



class ClusterSerializer(serializers.ModelSerializer):
	clusterag = CAGSerializer(many=True, read_only=True)

	class Meta:
		model = Cluster
		fields = ('id', 'name', 'district', 'municipality', 'ward', 'clusterag')


class ConfigSerializer(serializers.ModelSerializer):
	beneficiary_updated = serializers.SerializerMethodField()
	activity_updated = serializers.SerializerMethodField()

	def get_beneficiary_updated(self, obj):
		date = Beneficiary.objects.all().aggregate(Max('updated_at'))['updated_at__max']

		if date:
			return time.mktime(date.timetuple())*1000
		else:
			return 0

	def get_activity_updated(self, obj):
		date = obj.activity_group_updated
		return time.mktime(date.timetuple())*1000

	class Meta():
		model = Config
		fields = ('id', 'available_version', 'updates', 'beneficiary_updated', 'activity_updated') 

from rest_framework import serializers

from .models import ActivityGroup, Activity


class ActivitySerializer(serializers.ModelSerializer):
	class Meta:
		model = Activity
		fields = ('activity_group', 'name', 'description', 'AG_Id', 'target_number', 'target_unit', 'start_date', 'end_date', 'form_id', 'target_complete', 'beneficiary_level', 'published', 'target_met')
	
class ActivityGroupSerializer(serializers.ModelSerializer):
	activity = ActivitySerializer(many=True, read_only=True)

	class Meta:
		model = ActivityGroup
		fields = ('output', 'name', 'description', 'activity')
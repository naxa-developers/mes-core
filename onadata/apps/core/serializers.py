from rest_framework import serializers

from .models import ActivityGroup
	
class ActivityGroupSerializer(serializers.ModelSerializer):
	activity = serializers.StringRelatedField(many=True)

	class Meta:
		model = ActivityGroup
		fields = ('output', 'name', 'description', 'activity')
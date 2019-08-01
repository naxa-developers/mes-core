from django.core import serializers

GeoJSONSerializer = serializers.get_serializer("geojson")


class Serializer(GeoJSONSerializer):
    def get_dump_object(self, obj):
        data = super(Serializer, self).get_dump_object(obj)
        # Extend to your taste
        data['properties'].update(progress=obj.progress)
        return data

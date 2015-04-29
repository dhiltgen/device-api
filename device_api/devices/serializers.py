from rest_framework import serializers

# TODO - Try to figure out how to dynamically change
#        the fields, based on what's there
# http://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
class DeviceSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=50)
    type = serializers.CharField(max_length=20)
    family = serializers.CharField(max_length=3)
    #temp = serializers.FloatField()

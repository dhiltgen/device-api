from rest_framework import serializers
from rest_framework.reverse import reverse

import logging

log = logging.getLogger(__name__)


class SubdeviceSerializer(serializers.Serializer):
    device = serializers.CharField(max_length=50)
    label = serializers.CharField(max_length=50)
    reading = serializers.CharField(max_length=20)


class DeviceSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    type = serializers.CharField(max_length=20)
    family = serializers.CharField(max_length=3)
    subdevices = serializers.SerializerMethodField()

    def get_id(self, obj):
        return reverse('device-detail', kwargs={'device':obj.id},
                       request=self.context['request'])

    def get_subdevices(self, obj):
        return [reverse('subdevice', kwargs={'device':obj.id,
                                            'subdevice':x},
                       request=self.context['request'])
                for x in obj.subdevices]

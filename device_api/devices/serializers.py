from rest_framework import serializers
from rest_framework.reverse import reverse
import re

import logging

log = logging.getLogger(__name__)


class SubdeviceSerializer(serializers.Serializer):
    device = serializers.CharField()
    label = serializers.CharField()
    reading = serializers.SerializerMethodField()

    def get_reading(self, obj):
        """
        Attempt to figure out what the reading looks like and conver it
        """
        if re.match(r'\s*[0-9]+\s*$', obj.reading):
            return int(obj.reading)
        elif re.match(r'\s*[0-9]+\.[0-9]+\s*$', obj.reading):
            return float(obj.reading)
        else:
            return obj.reading


class DeviceSerializer(serializers.Serializer):
    server = serializers.CharField()
    id = serializers.SerializerMethodField()
    type = serializers.CharField()
    family = serializers.CharField()
    subdevices = serializers.SerializerMethodField()

    def get_id(self, obj):
        return reverse('device-detail', kwargs={'device':obj.id, 'server':obj.server},
                       request=self.context['request'])

    def get_subdevices(self, obj):
        return [reverse('subdevice', kwargs={'device':obj.id,
                                            'subdevice':x,
                                            'server':obj.server},
                       request=self.context['request'])
                for x in obj.subdevices]

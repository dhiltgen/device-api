from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from devices.serializers import DeviceSerializer, SubdeviceSerializer
from devices.models import get_all_devices, get_device, get_subdevice

import logging


log = logging.getLogger(__name__)

class ListDevices(APIView):
    def get(self, request, format=None):
        devices = get_all_devices()
        serializer = DeviceSerializer(devices, many=True,
                                      context={'request': request})
        return Response(serializer.data)


class DeviceDetail(APIView):
    def get_object(self, server, device):
        return get_device(device, server)

    def get(self, request, server, device, format=None):
        dev = self.get_object(server, device)
        serializer = DeviceSerializer(dev, context={'request': request})
        return Response(serializer.data)

class SubdeviceDetail(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_object(self, server, device, subdevice):
        return get_subdevice(device, subdevice, server)

    def get(self, request, server, device, subdevice, format=None):
        dev = self.get_object(server, device, subdevice)
        serializer = SubdeviceSerializer(dev, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, server, device, subdevice, format=None):
        dev = self.get_object(server, device, subdevice)
        # This isn't quite following the django rest idioms, but it works
        dev.set_reading(request.data['reading'])
        serializer = SubdeviceSerializer(dev, context={'request': request})
        return Response(serializer.data)

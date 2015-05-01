from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from devices.serializers import DeviceSerializer, SubdeviceSerializer
from devices.models import get_all_devices, get_device, get_subdevice

class ListDevices(APIView):
    #authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        devices = get_all_devices()
        serializer = DeviceSerializer(devices, many=True, context={'request': request})
        return Response(serializer.data)


class DeviceDetail(APIView):
    def get_object(self, device):
        return get_device(device)

    def get(self, request, device, format=None):
        dev = self.get_object(device)
        serializer = DeviceSerializer(dev, context={'request': request})
        return Response(serializer.data)

class SubdeviceDetail(APIView):
    def get_object(self, device, subdevice):
        return get_subdevice(device, subdevice)

    def get(self, request, device, subdevice, format=None):
        dev = self.get_object(device, subdevice)
        serializer = SubdeviceSerializer(dev, context={'request': request})
        return Response(serializer.data)


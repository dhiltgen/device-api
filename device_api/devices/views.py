from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from devices.serializers import DeviceSerializer
from devices.models import get_all_devices

class ListDevices(APIView):
    #authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        devices = get_all_devices()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)

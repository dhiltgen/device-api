from django.conf.urls import url, include
from devices import views

urlpatterns = [
    url(r'^device/$', views.ListDevices.as_view(), name='device-list'),
    url(r'^device/(?P<device>[^/]+)/$', views.DeviceDetail.as_view(), name='device-detail'),
    url(r'^device/(?P<device>[^/]+)/(?P<subdevice>[^/]+)$', views.SubdeviceDetail.as_view(), name='subdevice'),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


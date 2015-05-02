from django.conf.urls import url, include
from devices import views

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.ListDevices.as_view(), name='device-list'),
    url(r'^(?P<server>[^/]+)/(?P<device>[^/]+)/$', views.DeviceDetail.as_view(), name='device-detail'),
    url(r'^(?P<server>[^/]+)/(?P<device>[^/]+)/(?P<subdevice>[^/]+)$', views.SubdeviceDetail.as_view(), name='subdevice'),

]


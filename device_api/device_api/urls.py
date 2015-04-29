from django.conf.urls import url, include
from devices import views

urlpatterns = [
    url(r'^device/', views.ListDevices.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


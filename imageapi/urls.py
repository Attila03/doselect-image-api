from django.conf.urls import url

from .views import ImageListView, ImageDetailView

urlpatterns = [
    url(r'images/$', ImageListView.as_view(), name='image-list'),
    url(r'images/(?P<name>[^/\\]*\.\w+)/$', ImageDetailView.as_view(), name='image-detail'),
]
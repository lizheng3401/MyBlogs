from django.conf.urls import url

from . import views

app_name = 'blog'

urlpatterns = [
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
]
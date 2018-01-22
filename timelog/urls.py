from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.views.generic import TemplateView

from .views import (
    TimeLogListView, TimeLogDetailView, TimeLogCreateView, TimeLogUpdateView, TimeLogDeleteView
)
app_name = 'timelog'

urlpatterns = [
    url(r'list/^$',TimeLogListView.as_view(),name='list'),
    url(r'^add/$',TimeLogCreateView.as_view(),name='add'),
    url(r'^(?P<pk>\d+)/$',TimeLogUpdateView.as_view(),name='update'),
    url(r'^delete/(?P<pk>[\w]+)/$', TimeLogDeleteView.as_view(), name='delete')
]
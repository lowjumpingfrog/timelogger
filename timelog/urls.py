from django.conf.urls import url,include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import permission_required

from .views import (
    TimeLogListView, TimeLogDetailView, TimeLogCreateView, TimeLogUpdateView, TimeLogDeleteView , TimeLogReportView, TimeLogFormView, ReportView
)
app_name = 'timelog'

urlpatterns = [
    url(r'list/$',TimeLogListView.as_view(),name='list'),
    url(r'^add/$',TimeLogCreateView.as_view(),name='add'),
    url(r'^(?P<pk>\d+)/$',TimeLogUpdateView.as_view(),name='update'),
    url(r'^delete/(?P<pk>[\w]+)/$', TimeLogDeleteView.as_view(), name='delete'),
    url(r'^report/$',permission_required('is_staff')(TimeLogReportView.as_view()), name='report'),
    url(r'^report/view/(?P<report_start>[\w-]+)/(?P<report_end>[\w-]+)/$',permission_required('is_staff')(ReportView.as_view()), name='view'),

]

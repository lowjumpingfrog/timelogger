"""timelogger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, PasswordResetView, LogoutView
from timelog.views import HomeView
from django.contrib.admin import site
from django.conf.urls.static import static
from django.conf import settings

admin.site.site_header = "SPS Time Tracker"

handler404 = 'timelogger.views.handler404'
handler500 = 'timelogger.views.handler500'
handler400 = 'timelogger.views.handler400'
handler403 = 'timelogger.views.handler403'

urlpatterns = [
    url(r'^$',HomeView.as_view(),name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^timelog/', include('timelog.urls', namespace='timelog')),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url('admin/password_reset/',auth_views.PasswordResetView.as_view(),name='admin_password_reset',),
]

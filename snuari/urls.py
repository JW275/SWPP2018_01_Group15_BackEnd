"""snuari URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from snuariapi import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view()),
    url(r'^logout/$', views.LogoutView.as_view()),
    url(r'^me/$', views.UserSelfView.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetailView.as_view()),
    url(r'^club/$', views.ClubListView.as_view()),
    url(r'^club/(?P<pk>[0-9]+)/$', views.ClubDetailView.as_view()),
    url(r'^club/(?P<pk>[0-9]+)/join/$', views.ClubJoinView.as_view()),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^signup/$', views.SignupView.as_view()),
    url(r'^verify/$', views.VerifyView.as_view()),
    url(r'^event/$', views.EventListView.as_view(), name='event_list'),
    url(r'^event/(?P<pk>[0-9]+)/$', views.EventDetailView.as_view(), name='event_detail'),
    url(r'^event/(?P<pk>[0-9]+)/future_attendee/$', views.EventFutureAttendeeView.as_view(), name='event_future_attendee'),
    url(r'^event/(?P<pk>[0-9]+)/future_absentee/$', views.EventFutureAbsenteeView.as_view(), name='event_future_absentee'),
    url(r'^event/(?P<pk>[0-9]+)/past_attendee/$', views.EventPastAttendeeView.as_view(), name='event_past_attendee'),

]

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
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^me/$', views.UserSelfView.as_view(), name='user_self'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetailView.as_view(), name='user_detail'),
    url(r'^club/$', views.ClubListView.as_view(), name='club_list'),
    url(r'^club/(?P<pk>[0-9]+)/$', views.ClubDetailView.as_view(), name='club_detail'),
    url(r'^club/(?P<pk>[0-9]+)/join/$', views.ClubJoinView.as_view(), name='club_join'),
    url(r'^club/(?P<club_id>[0-9]+)/member/(?P<uid>[0-9]+)/$', views.ClubMemberView.as_view(), name='club_member'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^verify/$', views.VerifyView.as_view(), name='verify'),
    url(r'^board/$', views.BoardListView.as_view(), name='board_list'),
    url(r'^board/(?P<pk>[0-9]+)/$', views.BoardDetailView.as_view(), name='board_detail'),
    url(r'^article/$', views.ArticleListView.as_view(), name='article_list'),
    url(r'^article/(?P<pk>[0-9]+)/$', views.ArticleDetailView.as_view(), name='article_detail'),
    url(r'^comment/$', views.CommentListView.as_view(), name='comment_list'),
    url(r'^comment/(?P<pk>[0-9]+)/$', views.CommentDetailView.as_view(), name='comment_detail'),
    url(r'^account/$', views.AccountingListView.as_view()),
    url(r'^account/(?P<pk>[0-9]+)/$', views.AccountingDetailView.as_view()),
    url(r'^account/statistic/(?P<pk>[0-9]+)/$', views.AccountingStatisticView.as_view()),
    url(r'^api-auth/', include('rest_framework.urls')),
]

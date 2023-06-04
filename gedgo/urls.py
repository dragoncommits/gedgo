from django.urls import re_path
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordResetView

from gedgo import views

urlpatterns = [
    re_path(
        r'^(?P<gedcom_id>\d+)/(?P<person_id>I\d+)/$',
        views.person,
        name='person'
    ),
    re_path(r'^(?P<gedcom_id>\d+)/$', views.gedcom, name='gedcom'),

    # XHR Data views
    re_path(r'^(?P<gid>\d+)/pedigree/(?P<pid>I\d+)/$', views.pedigree),
    re_path(r'^(?P<gid>\d+)/timeline/(?P<pid>I\d+)/$', views.timeline),
    re_path(r'^dashboard/worker/status$', views.worker_status),

    re_path(r'^blog/$', views.blog_list),
    re_path(r'^blog/(?P<year>\d+)/(?P<month>\d+)/$', views.blog),
    re_path(r'^blog/post/(?P<post_id>\d+)/$', views.blogpost),
    re_path(r'^documentaries/$', views.documentaries),
    re_path(r'^documentaries/(?P<title>.+)/$', views.documentary_by_id),
    re_path(r'^document/(?P<doc_id>\w+)/$', views.document),
    re_path(r'^research/(?P<pathname>.*)$', views.research),
    re_path(r'^search/$', views.search),
    re_path(r'^dashboard/$', views.dashboard),

    # Auth
    re_path(r'^logout/$', views.logout_view),
    re_path(r'^password_reset/$', PasswordResetView.as_view(
        subject_template_name='email/password_reset_subject.txt',
        email_template_name='auth/password_reset_email.txt',
        html_email_template_name='email/password_reset.html',
    ), name='auth_password_reset'),
    # Authenticated media fileserve view
    re_path(r'^media/(?P<storage_name>\w+)/(?P<pathname>.*)$', views.media),

    re_path(r'^$', lambda r: redirect('/gedgo/1/')),
]

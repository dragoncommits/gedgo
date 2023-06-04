from django.urls import include, re_path
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = [
    re_path(r'^$', lambda r: redirect('/gedgo/')),
    re_path(r'^gedgo/', include('gedgo.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^accounts/login/$', LoginView.as_view(),
        {'template_name': 'auth/login.html'}),
    re_path(r'^login/$', LoginView.as_view(),
        {'template_name': 'auth/login.html'}),
    re_path(r'^robots\.txt$',
        lambda r: HttpResponse(
            "User-agent: *\nDisallow: /",
            mimetype="text/plain"))
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

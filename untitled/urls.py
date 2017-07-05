"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from untitled import views
from untitled import settings
from django.conf.urls.static import static

urlpatterns = [
 
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.main),
    url(r'^contact/$', views.contact),
    url(r'^sign_in/$', views.login),
    url(r'^register/$', views.register),
    url(r'^guest/$', views.guest),
    url(r'^logout/$', views.logout),
    url(r'^mykino/$', views.mykino),
    url(r'^otziv/(\w+)/$', views.otziv),
    url(r'^price/$', views.price),
    url(r'^film/(\w+)/$', views.seans),
    url(r'^soon/$', views.soon),
    url(r'^printbilet/$', views.print_bilet),
    url(r'^treler/(\w+)/$', views.treler),
    url(r'^kabinet/$', views.kabinet),
    url(r'^kabinet/page/(\d+)/$', views.kabinet),
    url(r'^soon/page/(\d+)/$', views.soon),
    url(r'^buy/seans/seans_id=(\d+)/$', views.buy),
    url(r'^printotchet/(\w+)/$', views.print_otchet),
    url(r'^(?P<url_date>[\w-]+)/page/(?P<page_number>\d+)/$', views.main),
    url(r'^(?P<url_date>[\w-]+)/$', views.main),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)

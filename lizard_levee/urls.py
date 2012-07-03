# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin
from lizard_ui.urls import debugmode_urlpatterns

from lizard_levee import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^ui/', include('lizard_ui.urls')),
    url(r'^map/', include('lizard_map.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',
        views.Overview.as_view(),
        name='lizard_geodin_overview'),
    url(r'^(?P<slug>[^/]+)/$',
        views.BurgomasterView.as_view(),
        name='lizard_geodin_burgomaster'),
    # url(r'^something/',
    #     views.some_method,
    #     name="name_it"),
    )
urlpatterns += debugmode_urlpatterns()

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
    # url(r'^$',
    #     views.HomepageView.as_view(),
    #     name='lizard_levee_homepage'),
    url(r'^$',
        views.Overview.as_view(),
        name='lizard_levee_overview'),

    url(r'^image-map/$',
        views.ImageMapListView.as_view(),
        name='lizard_levee_image_map_list'),
    url(r'^image-map/(?P<slug>[^/]+)/$',
        views.ImageMapView.as_view(),
        name='lizard_levee_image_map'),
    url(r'^image-map/(?P<slug>[^/]+)/map/$',
        views.ImageMapMapView.as_view(),
        name='lizard_levee_image_map_map'),

    url(r'^message-box/$',
        views.MessageBoxListView.as_view(),
        name='lizard_levee_message_box_list'),
    url(r'^message-box/(?P<slug>[^/]+)/$',
        views.MessageBoxView.as_view(),
        name='lizard_levee_message_box'),

    url(r'^links/(?P<slug>[^/]+)/$',
        views.LinkSetView.as_view(),
        name='lizard_levee_links'),
    url(r'^files/$',
        views.UploadedFileView.as_view(),
        name='lizard_levee_uploaded_files'),
    url(r'^information_pointer/(?P<slug>[^/]+)/$',
        views.InformationPointerView.as_view(),
        name='lizard_levee_information_pointer'),
    url(r'^filters/$',
        views.FilterView.as_view(),
        name='lizard_levee_filters'),
    url(r'^pointset/$',
        views.PointSetListView.as_view(),
        name='lizard_levee_pointset_list'),
    url(r'^pointset/(?P<slug>[^/]+)/$',
        views.PointSetView.as_view(),
        name='lizard_levee_pointset'),
    url(r'^risktable/$',
        views.RiskTableView.as_view(),
        name='lizard_levee_risk_table'),

    url(r'^tools/convert/$',
        views.ConvertView.as_view(),
        name='lizard_levee_tools_convert'),
    url(r'^tools/harvest/$',
        views.HarvestView.as_view(),
        name='lizard_levee_tools_harvest'),

    url(r'^(?P<slug>[^/]+)/$',
        views.BurgomasterView.as_view(),
        name='lizard_levee_burgomaster'),
    url(r'^(?P<slug>[^/]+)/expert/$',
        views.ExpertView.as_view(),
        name='lizard_levee_expert'),
    # url(r'^(?P<slug>[^/]+)/risk_geojson/$',
    #     views.risk_geojson,
    #     name='lizard_levee_risk_geojson'),
    # url(r'^something/',
    #     views.some_method,
    #     name="name_it"),
    )
urlpatterns += debugmode_urlpatterns()

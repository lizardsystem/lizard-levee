# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals

# from django.utils.translation import ugettext as _
from django.contrib.gis import admin
from sorl.thumbnail.admin import AdminImageMixin

from lizard_levee import models


class ImageMapLinkInline(admin.TabularInline):
    model = models.ImageMapLink


class AreaAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('slug', 'name')
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ('wms_layers', 'information_pointers', 'links')


class InformationPointerAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('slug', 'title', 'more_url')
    list_editable = ('title', 'more_url')
    prepopulated_fields = {"slug": ("title",)}


class LinkSetAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}


class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url')
    list_editable = ('title', 'url')


class SegmentAdmin(admin.GeoModelAdmin):
    list_display = ('id', 'area', 'segment_id', 'risk')
    list_editable = ('risk',)


class ImageMapAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", )}
    inlines = [ImageMapLinkInline, ]


class MessageTagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"tag": ("name",)}


class MessageBoxAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(models.MessageTag, MessageTagAdmin)
admin.site.register(models.Message)
admin.site.register(models.MessageBox, MessageBoxAdmin)

admin.site.register(models.ImageMapGroup)
admin.site.register(models.ImageMap, ImageMapAdmin)

admin.site.register(models.Link, LinkAdmin)
admin.site.register(models.LinkSet, LinkSetAdmin)

admin.site.register(models.Area, AreaAdmin)
admin.site.register(models.InformationPointer, InformationPointerAdmin)
admin.site.register(models.Segment, SegmentAdmin)

# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext as _
from sorl.thumbnail.admin import AdminImageMixin

from lizard_levee import models


class AreaAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ('wms_layers', 'information_pointers', 'links')


class InformationPointerAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('slug', 'title', 'more_url')
    list_editable = ('title', 'more_url')
    prepopulated_fields = {"slug": ("title",)}


class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url')
    list_editable = ('title', 'url')


admin.site.register(models.Area, AreaAdmin)
admin.site.register(models.InformationPointer, InformationPointerAdmin)
admin.site.register(models.Link, LinkAdmin)

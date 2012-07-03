# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext as _

from lizard_levee import models


class AreaAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(models.Area, AreaAdmin)

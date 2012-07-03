# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals

# from django.core.urlresolvers import reverse
# from lizard_ui.views import UiView
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from lizard_map.views import MapView
import lizard_geodin.models

from lizard_levee import models


class Overview(MapView):
    """Overview of our areas for which we have further views."""
    template_name = 'lizard_levee/overview.html'
    page_title = _('Overview of areas')


class BurgomasterView(MapView):
    """The main non-technical view on a Geodin levee project."""
    template_name = 'lizard_levee/burgomaster.html'

    @property
    def area(self):
        return get_object_or_404(models.Area, slug=self.kwargs['slug'])

    @property
    def page_title(self):
        return _('Overview of {name}').format(
            name=self.area.name)

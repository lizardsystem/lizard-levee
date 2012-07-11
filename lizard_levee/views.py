# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals

# import lizard_geodin.models
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from lizard_map.views import MapView
from lizard_ui.layout import Action
from lizard_ui.views import UiView

from lizard_levee import models


class Overview(MapView):
    """Overview of our areas for which we have further views."""
    template_name = 'lizard_levee/overview.html'
    page_title = _('Overview of areas')
    edit_link = '/admin/lizard_levee/area/'

    def areas(self):
        """Return all areas."""
        return models.Area.objects.all()


class BurgomasterView(MapView):
    """The main non-technical view on a Geodin levee project."""
    template_name = 'lizard_levee/burgomaster.html'

    @property
    def area(self):
        return get_object_or_404(models.Area, slug=self.kwargs['slug'])

    @property
    def edit_link(self):
        return '/admin/lizard_levee/area/{0}'.format(self.area.pk)

    @property
    def page_title(self):
        return _('Overview of {name}').format(
            name=self.area.name)

    @property
    def information_pointers(self):
        # TODO: should we limit the number of items?
        return self.area.information_pointers.all()

    @property
    def links(self):
        # TODO: should we limit the number of items?
        return self.area.links.all()

    @property
    def link_to_other(self):
        """Return action that links to the other (=expert) page."""
        action = Action(
            name=_("Expert page"),
            url=reverse('lizard_levee_expert',
                        kwargs={'slug': self.kwargs['slug']}),
            icon='icon-random',
            )
        return action

    @property
    def content_actions(self):
        actions = [self.link_to_other]
        actions += super(BurgomasterView, self).content_actions
        return actions

    def extra_wms_layers(self):
        wms_sources = self.area.wms_layers.all()
        if not wms_sources:
            return
        result = []
        for wms_source in wms_sources:
            result.append({'wms_id': wms_source.id,
                           'name': wms_source.name,
                           'url': wms_source.url,
                           'params': wms_source.params,
                           'options': wms_source.options,
                           })
        return result


class ExpertView(BurgomasterView):
    """The view for expert: more data, more graphs."""
    template_name = 'lizard_levee/expert.html'

    @property
    def page_title(self):
        return _('Expert view for {name}').format(
            name=self.area.name)

    @property
    def link_to_other(self):
        """Return action that links to the other (=burgomaster) page."""
        action = Action(
            name=_("Overview page"),
            url=reverse('lizard_levee_burgomaster',
                        kwargs={'slug': self.kwargs['slug']}),
            icon='icon-random',
            )
        return action

    @property
    def sensor_types(self):
        # Probably I should switch this name to something else.
        # This list filters the page contents (especially the graph).
        return [
            'temperatuur',
            'debiet',
            'waterpeil',
            'waterspanning',
            'verdraaiing',
            'trilling',
            'voltmeting',
            'rek/deformatie',
            ]

    @property
    def cross_sections(self):
        """Return cross sections (in addition to selecting them in the map).
        """
        return ['A-A', 'B-B', 'C-C']

    @property
    def longitudinal_sections(self):
        """Return longitudinal cross sections.
        """
        return ['Lengtedoorsnede']

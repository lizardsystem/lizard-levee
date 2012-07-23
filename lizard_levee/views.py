# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import logging

# from django.core.urlresolvers import reverse
# from django.http import HttpResponse
# from lizard_ui.layout import Action
# from lizard_ui.views import UiView
# import lizard_geodin.models
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from lizard_map.views import MapView
from lizard_map.views import HomepageView
from lizard_map.models import WorkspaceEditItem
from lizard_ui.layout import Action
from lizard_ui.views import UiView

from lizard_levee import models


logger = logging.getLogger(__name__)


class SiteActionView(MapView):
    """Inherit from this view to enable 'tabs'"""
    @property
    def site_actions(self):
        actions = []
        actions.append(
            Action(
                name='burgemeester',
                description='burgemeester',
                url='/levee/piping-proef/',
                icon='icon-folder-close'))

        actions.append(
            Action(
                name='expert',
                description='expert',
                url='/levee/piping-proef/expert/',
                icon='icon-folder-open'))

        actions.append(
            Action(
                name='kaart',
                description='kaart',
                icon='icon-map-marker'))
        return actions + super(SiteActionView, self).site_actions


# class HomepageView(SiteActionView, HomepageView):
#     pass
class HomepageView(SiteActionView, UiView):
    """
    Selector for burgermeester, expert, kaart.
    """
    template_name = 'lizard_levee/homepage.html'


class Overview(SiteActionView, MapView):
    """Overview of our areas for which we have further views."""
    template_name = 'lizard_levee/overview.html'
    page_title = _('Overview of areas')
    edit_link = '/admin/lizard_levee/area/'

    def areas(self):
        """Return all areas."""
        return models.Area.objects.all()


class BurgomasterView(SiteActionView, MapView):
    """The main non-technical view on a Geodin levee project."""
    template_name = 'lizard_levee/burgomaster.html'
    map_div_class = 'map-at-top i-have-height'
    workspace_on_top = True

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

    def extra_wms_layers(self):
        self.insert_risk_layer()
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

    def insert_risk_layer(self):
        special_name = self.area.slug + ' risk layer'
        workspace = self.workspace()
        if workspace.workspace_items.filter(name=special_name).exists():
            return
        adapter_json = '{"slug": "%s"}' % self.area.slug
        workspace_item = WorkspaceEditItem(
            workspace=workspace,
            name=special_name,
            adapter_class='lizard_levee_risk_adapter',
            adapter_layer_json=adapter_json,
            index=200)
        workspace_item.save()
        logger.debug("Added special workspace item")


class ExpertView(BurgomasterView):
    """The view for expert: more data, more graphs.

    The basic setup is that you always have a map on top where you can select
    levee segments. There are three different subviews:

    - The default: a big graph with the values for the selected levee
      segment. Perhaps also more info if a failure measure is attached to the
      chosen segment.

    - A cross section where you can, when we have 'em, select sensors. Their
      data is shown underneath.

    - Similarly for the longitudinal cross section.

    """
    template_name = 'lizard_levee/expert.html'

    @property
    def page_title(self):
        return _('Expert view for {name}').format(
            name=self.area.name)

    @property
    def breadcrumbs(self):
        """Return homepage + ourselves as breadcrumbs."""
        result = super(ExpertView, self).breadcrumbs
        result.append(self.our_own_breadcrumb_element)
        return result

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
    def display_options(self):
        """Return information for changing the display of the page.

        Kind, subitem, title
        """
        result = []
        result.append({'subitem': None,
                       'show': '#expert-graph',
                       'hide1': '#cross-section',
                       'hide2': '#longitudinal-cross-section',
                       'title': _("Big graph")})
        for cross_section in ['A-A', 'B-B', 'C-C']:
            title = _("Cross section {title}").format(title=cross_section)
            result.append({'subitem': cross_section,
                           'hide1': '#expert-graph',
                           'show': '#cross-section',
                           'hide2': '#longitudinal-cross-section',
                           'title': title})
        result.append({'subitem': None,
                       'hide2': '#expert-graph',
                       'hide1': '#cross-section',
                       'show': '#longitudinal-cross-section',
                       'title': _('Longitudinal cross section')})
        return result

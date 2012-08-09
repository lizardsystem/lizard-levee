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
from lizard_ui.views import ViewContextMixin
from django.views.generic.base import TemplateView
from django.views.generic.base import View

from lizard_levee import models
from PIL import Image, ImageDraw
from django.http import HttpResponse
import lizard_geodin.models

from lizard_map import coordinates

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
                url='/map/',
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

    @property
    def sidebar_actions(self):
        return []

    @property
    def rightbar_actions(self):
        return []

    # map_div_class = 'give-me-height'


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


class ImageMapListView(UiView):
    template_name = 'lizard_levee/image_map_list.html'

    @property
    def image_maps(self):
        return models.ImageMap.objects.exclude(group=None)

    @property
    def image_map_groups(self):
        return models.ImageMapGroup.objects.all()

    @property
    def image_map(self):
        return self.image_maps[0]


class ImageMapView(ViewContextMixin, TemplateView):
    template_name = 'lizard_levee/image_map.html'

    @property
    def image_map(self):
        return get_object_or_404(models.ImageMap, slug=self.kwargs['slug'])


class ImageMapMapView(View):
    """
    A png with the map as image
    """
    def get(self, request, **kwargs):

        image_map = get_object_or_404(models.ImageMap, slug=self.kwargs['slug'])

        size = (image_map.image_width, image_map.image_height)             # size of the image to create
        im = Image.new('RGBA', size) # create the image
        draw = ImageDraw.Draw(im)   # create a drawing object that is
                                    # used to draw on the new image
        for image_map_link in image_map.imagemaplink_set.all():
            # See if the image_map_link passes the filter criteria in the session
            filters = {}
            try:
                filters = request.session['filter-measurements']
            except:
                pass
            # if image_map_link.measurement:
            #     filter_key = 'Project::%d' % image_map_link.measurement.project.id
            #     if filter_key in filters and filters[filter_key] == 'false':
            #         # This object is unwanted.
            #         continue

            # Filter points
            if image_map_link.points:
                some_are_wanted = False
                for point in image_map_link.points.all():
                    filter_key = 'Supplier::%d' % point.measurement.supplier.id
                    filter_key_param = 'Parameter::%d' % point.measurement.parameter.id
                    if ((filter_key not in filters or filters[filter_key] == 'true') and
                        (filter_key_param not in filters or filters[filter_key_param] == 'true')):
                        # This object is wanted.
                        some_are_wanted = True
                if not some_are_wanted:
                    # If none of the points are wanted.. don't draw
                    continue

            # If it passes, the code below will run
            coords = [int(c) for c in image_map_link.coords.split(',')]

            if image_map_link.shape == 'circle':
                draw.ellipse((
                        coords[0]-coords[2], coords[1]-coords[2],
                        coords[0]+coords[2], coords[1]+coords[2]),
                             outline=(0, 0, 0, 255),
                             fill=(0, 255, 0, 255))
            elif image_map_link.shape == 'rect':
                draw.rectangle(coords,
                             outline=(0, 0, 0, 255),
                             fill=(0, 255, 0, 255))
            elif image_map_link.shape == 'polygon':
                draw.polygon(coords,
                             outline=(0, 0, 0, 255),
                             fill=(0, 255, 0, 255))

        del draw # I'm done drawing so I don't need this anymore

        # We need an HttpResponse object with the correct mimetype
        response = HttpResponse(mimetype="image/png")
        # now, we tell the image to save as a PNG to the
        # provided file-like object
        im.save(response, 'PNG')

        return response # and we're done!


class MessageBoxListView(UiView):
    template_name = 'lizard_levee/message_box_list.html'

    @property
    def message_box_list(self):
        return models.MessageBox.objects.all()


class MessageBoxView(UiView):
    template_name = 'lizard_levee/message_box.html'

    @property
    def message_box(self):
        return get_object_or_404(models.MessageBox, slug=self.kwargs['slug'])

    def filters(self):
        filters = {}
        try:
            filters = self.request.session['filter-tags']
        except:
            pass
        return filters

    def tags_checked(self):
        """Return list with 2-tuples: (tag, checked) """
        filters = self.filters()
        def tag_checked(o):
            if o.tag not in filters or filters[o.tag] == 'true':
                return True
            else:
                return False
        return [(o, tag_checked(o)) for o in models.MessageTag.objects.all()]

    def messages(self):
        filters = self.filters()
        tags = []
        for tag, checked in self.tags_checked():
            if checked:
                tags.append(tag)
        return models.Message.objects.filter(tags__in=tags)

    def post(self, request, *args, **kwargs):

        filters = dict([(v, k) for v, k in request.POST.items()])
        request.session['filter-tags'] = filters

        return super(MessageBoxView, self).get(request, *args, **kwargs)


class LinkSetView(ViewContextMixin, TemplateView):
    template_name = 'lizard_levee/link_set.html'

    @property
    def link_set(self):
        return get_object_or_404(models.LinkSet, slug=self.kwargs['slug'])


class InformationPointerView(ViewContextMixin, TemplateView):
    template_name = 'lizard_levee/information_pointer.html'

    @property
    def information_pointer(self):
        return get_object_or_404(models.InformationPointer, slug=self.kwargs['slug'])


class FilterView(ViewContextMixin, TemplateView):
    """
    Filters measurement points on some criteria, store it in the session.

    You get <name>::<data-id> as key, u'true' or u'false' as value
    """

    template_name = 'lizard_levee/filter.html'

    @property
    def filter_groups(self):
        """return a list of dicts with keys name and data.

        Data is a 2-tuple list with objects and wether the object has
        to be checked.
        """
        filters = {}
        try:
            filters = self.request.session['filter-measurements']
        except:
            pass
        def supplier_checked(o):
            key = 'Supplier::%d' % o.id
            if key not in filters or filters[key] == 'true':
                return True
            else:
                return False
        def parameter_checked(o):
            key = 'Parameter::%d' % o.id
            if key not in filters or filters[key] == 'true':
                return True
            else:
                return False
        result = [{'name': 'Leverancier',
                   'data_name': 'Supplier',
                   'data': [(o, supplier_checked(o)) for o in lizard_geodin.models.Supplier.objects.all()]},
                  {'name': 'Parameter',
                   'data_name': 'Parameter',
                   'data': [(o, parameter_checked(o)) for o in lizard_geodin.models.Parameter.objects.all()]}
            ]
        return result

    def post(self, request, *args, **kwargs):
        print 'post filters ------------------------------------------>'
        # You get <name>::<data-id> as key, u'true' or u'false' as value
        # print request.POST

        filters = dict([(v, k) for v, k in request.POST.items()])
        request.session['filter-measurements'] = filters
        print filters

        return super(FilterView, self).get(request, *args, **kwargs)


class ConvertView(UiView):
    """
    A tool to convert coordinates
    """
    template_name = 'lizard_levee/convert.html'

    def post(self, request, *args, **kwargs):
        post = request.POST
        message_list = ["result: ", ]
        try:
            google_x = float(post['google_x'])
            google_y = float(post['google_y'])
            c_rd = coordinates.google_to_rd(google_x, google_y)
            message_list.append('Google (%s, %s) = RD (%s, %s)' % (
                    google_x, google_y, c_rd[0], c_rd[1]))
            c_wgs84 = coordinates.google_to_wgs84(google_x, google_y)
            message_list.append('Google (%s, %s) = WGS84 (%s, %s)' % (
                    google_x, google_y, c_wgs84[0], c_wgs84[1]))
        except:
            pass

        try:
            rd_x = float(post['rd_x'])
            rd_y = float(post['rd_y'])
            c_google = coordinates.rd_to_google(rd_x, rd_y)
            message_list.append('RD (%s, %s) = Google (%s, %s)' % (
                    rd_x, rd_y, c_google[0], c_google[1]))
            c_wgs84 = coordinates.rd_to_wgs84(rd_x, rd_y)
            message_list.append('RD (%s, %s) = WGS84 (%s, %s)' % (
                    rd_x, rd_y, c_wgs84[0], c_wgs84[1]))
        except:
            pass

        try:
            wgs84_x = float(post['wgs84_x'])
            wgs84_y = float(post['wgs84_y'])
            c_google = coordinates.wgs84_to_google(wgs84_x, wgs84_y)
            message_list.append('WGS84 (%s, %s) = Google (%s, %s)' % (
                    wgs84_x, wgs84_y, c_google[0], c_google[1]))
            c_rd = coordinates.wgs84_to_rd(wgs84_x, wgs84_y)
            message_list.append('WGS84 (%s, %s) = RD (%s, %s)' % (
                    wgs84_x, wgs84_y, c_rd[0], c_rd[1]))
        except:
            pass

        self.message = '<br/>'.join(message_list)
        return super(ConvertView, self).get(request, *args, **kwargs)

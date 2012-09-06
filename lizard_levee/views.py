# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import logging
import os
import pkg_resources

# from django.core.urlresolvers import reverse
# from django.http import HttpResponse
# from lizard_ui.views import UiView
from PIL import Image, ImageDraw
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from lizard_map import coordinates
from lizard_map.models import WorkspaceEditItem
from lizard_map.views import MapView
from lizard_ui.views import UiView
from lizard_ui.views import ViewContextMixin
import lizard_geodin.models

from lizard_levee import models

# for HarvestView
from django.core.management import call_command

logger = logging.getLogger(__name__)


class HomepageView(UiView):
    """
    Selector for burgermeester, expert, kaart.

    TODO: seems unused now. [reinout]

    """
    template_name = 'lizard_levee/homepage.html'


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
        result = models.ImageMapGroup.objects.all()

        group = self.request.GET.get('group', None)
        if group:
            result = result.filter(title=group)
        return result

    @property
    def image_map(self):
        """Return user-selected or first available image map."""
        slug = self.request.GET.get('slug', None)
        if slug:
            return get_object_or_404(models.ImageMap, slug=slug)

        for image_map_group in self.image_map_groups:
            if image_map_group.imagemap_set.exists():
                return image_map_group.imagemap_set.all()[0]


class ImageMapView(ViewContextMixin, TemplateView):
    template_name = 'lizard_levee/image_map.html'

    @property
    def image_map(self):
        """
        The default image map to be shown
        """
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
            fill_color = (200, 200, 200, 255)  # default color
            fill_max_value = -10000
            outline_color = (0, 0, 0, 255)  # default color

            # check if some points are wanted. Points are old, use ordered points instead.
            if (image_map_link.points or image_map_link.ordered_points) and not image_map_link.target_url:
                some_are_wanted = False
                # Coloring: this is the only info we got
                # Groen 0-50%; geel 50-74%; oranje 75-99%; rood 100% en daarboven
                image_map_link_points = image_map_link.imagemaplinkpoint_set.all().order_by('index')
                ordered_points = [imlp.point for imlp in image_map_link_points]

                for i, point in enumerate(ordered_points +
                                          list(image_map_link.points.all())):
                    filter_key = 'Supplier::%d' % point.measurement.supplier.id
                    filter_key_param = 'Parameter::%d' % point.measurement.parameter.id
                    if ((filter_key not in filters or filters[filter_key] == 'true') and
                        (filter_key_param not in filters or filters[filter_key_param] == 'true')):
                        # This object is wanted.
                        some_are_wanted = True
                        # Color fill: color on first point!
                        if image_map_link.color_me and i==0:
                            try:
                                point_last_value = point.last_value()
                                if image_map_link.color_legend:
                                    for legend_section in image_map_link.color_legend.imagemaplegendsection_set.all():
                                        legend_section_matches = True  # true until proven otherwise
                                        if legend_section.value_lower is not None:
                                            if point_last_value < legend_section.value_lower:
                                                legend_section_matches = False
                                        if legend_section.value_upper is not None:
                                            if point_last_value >= legend_section.value_upper:
                                                legend_section_matches = False
                                        if legend_section_matches:
                                            fill_color = legend_section.html_color
                                            break
                                else:
                                    # Default legend
                                    if point_last_value >= 2:
                                        fill_color = (64, 255, 64, 255)  # green
                                    elif point_last_value >= 1.5 and point_last_value < 2:
                                        fill_color = (255, 255, 64, 255)  # yellow
                                    elif point_last_value >= 1.25 and point_last_value < 1.5:
                                        fill_color = (255, 196, 48, 255)  # light orange
                                    elif point_last_value >= 1 and point_last_value < 1.25:
                                        fill_color = (255, 128, 32, 255)  # orange
                                    elif point_last_value >= 0.5 and point_last_value < 1:
                                        fill_color = (255, 32, 32, 255)  # light red
                                    elif point_last_value < 0.5:
                                        fill_color = (255, 0, 0, 255)  # really red
                            except:
                                # call failed: do not crash the whole image
                                fill_color = (150, 150, 150, 255)  # dark grey to show that we tried to use a legend
                                pass
                        # Color outline: supplier
                        if i == 0:
                            outline_color = point.measurement.supplier.html_color

                if not some_are_wanted:
                    # If none of the points are wanted.. don't draw
                    continue

            if image_map_link.target_url and image_map_link.target_outline_color:
                outline_color = image_map_link.target_outline_color

            # If it passes, the code below will run
            coords = [int(c) for c in image_map_link.coords.split(',')]

            if image_map_link.shape == 'circle':
                # Fake thicker outline with white
                outline_add_thickness = 1
                draw.ellipse((
                        coords[0] - coords[2] - outline_add_thickness - 2,
                        coords[1] - coords[2] - outline_add_thickness - 2,
                        coords[0] + coords[2] + outline_add_thickness + 2,
                        coords[1] + coords[2] + outline_add_thickness + 2),
                             outline=(255, 255, 255, 255),
                             fill=(255, 255, 255, 255))
                draw.ellipse((
                        coords[0] - coords[2] - outline_add_thickness,
                        coords[1] - coords[2] - outline_add_thickness,
                        coords[0] + coords[2] + outline_add_thickness,
                        coords[1] + coords[2] + outline_add_thickness),
                             outline=outline_color,
                             fill=outline_color)
                draw.ellipse((
                        coords[0] - coords[2], coords[1] - coords[2],
                        coords[0] + coords[2], coords[1] + coords[2]),
                             outline=outline_color,
                             fill=fill_color)
            elif image_map_link.shape == 'rect':
                draw.rectangle(coords,
                             outline=outline_color,
                             fill=fill_color)
            elif image_map_link.shape == 'polygon':
                draw.polygon(coords,
                             outline=outline_color,
                             fill=fill_color)

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
        return [(o, tag_checked(o)) for o in self.message_box.tags.all()]

    def messages(self):
        # filters = self.filters()
        tags = []
        for tag, checked in self.tags_checked():
            if checked:
                tags.append(tag)
        return models.Message.objects.filter(tags__in=tags)

    @property
    def popup(self):
        """Show tags on top?
        """
        return self.request.GET.get('popup', 'false') == 'true'

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
                   'data': [(o, supplier_checked(o)) for o in lizard_geodin.models.Supplier.objects.all().order_by('name')]},
                  {'name': 'Parameter',
                   'data_name': 'Parameter',
                   'data': [(o, parameter_checked(o)) for o in lizard_geodin.models.Parameter.objects.all().order_by('name')]}
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


class ToolOverview(UiView):
    """Helper page pointing at admin-level tools."""
    template_name = 'lizard_levee/tools.html'


class ImagemapToolView(UiView):
    """Helper page showing available image map images."""
    template_name = 'lizard_levee/tool-imagemaps.html'

    def imagemaps(self):
        image_dir = pkg_resources.resource_filename(
            'lizard_levee', 'static/lizard_levee/doorsnedes')
        filenames = [f for f in os.listdir(image_dir) if f.endswith('.png')]
        db_string = '/static_media/lizard_levee/doorsnedes/{filename}'
        return [db_string.format(filename=filename) for filename in filenames]


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


class HarvestView(UiView):
    """
    A tool to trigger some admin commands:

    - harvest twitter
    - harvest email
    """

    template_name = "lizard_levee/harvest.html"

    def post(self, request, *args, **kwargs):
        # Note: in production, twitter is refreshed every 5 minutes via a
        # cronjob. [reinout]
        message_list = ['wat ik heb gedaan:', ]

        result = call_command('levee_update_twitter', interactive=False)

        self.message = '<br/>'.join(message_list)
        return super(HarvestView, self).get(request, *args, **kwargs)


class PointSetListView(UiView):
    template_name = "lizard_levee/pointset-list.html"

    @property
    def pointsets(self):
        selected_pointset = self.selected_pointset
        return [(ps, ps==selected_pointset)
                for ps in models.PointSet.objects.all()]

    @property
    def selected_pointset(self):
        try:
            point_set_id = self.request.session['selected_point_set']
            point_set = models.PointSet.objects.get(pk=point_set_id)
        except:
            point_set = models.PointSet.objects.all()[0]
        return point_set

    @property
    def width(self):
        return self.selected_pointset.width

    @property
    def height(self):
        return self.selected_pointset.height

    @property
    def checked_points(self):
        def point_is_checked(pointset, point):
            try:
                return self.request.session['selected_point_set_point'][(pointset.id, point.id)]
            except:
                return True
        selected_pointset = self.selected_pointset
        return [(p, point_is_checked(selected_pointset, p)) for p in selected_pointset.points.all()]

    def post(self, request, *args, **kwargs):
        """
        Select a point set, or a single point in a point set.
        """
        # Check if we set the point_set
        point_set_id = request.POST.get("point_set", None)
        if point_set_id:
            request.session['selected_point_set'] = point_set_id

        # Click on single point
        point_from_point_set = request.POST.get("point_from_point_set", None)
        point_id = request.POST.get("point", None)
        point_checked = request.POST.get("point_checked", None)
        if point_from_point_set is not None and point_id is not None and point_checked is not None:
            if 'selected_point_set_point' in request.session:
                point_set_points = request.session['selected_point_set_point']
            else:
                point_set_points = {}
            point_set_points[(int(point_from_point_set), int(point_id))] = point_checked == 'true'
            request.session['selected_point_set_point'] = point_set_points

        return self.get(request, *args, **kwargs)

    @property
    def popup(self):
        """Show graphs big?
        """
        return self.request.GET.get('popup', 'false') == 'true'


class PointSetView(ViewContextMixin, TemplateView):
    template_name = 'lizard_levee/pointset.html'

    @property
    def pointset(self):
        return get_object_or_404(models.PointSet,
                                 slug=self.kwargs['slug'])

    @property
    def width(self):
        # image width
        return self.pointset.width

    @property
    def iframe_width(self):
        return self.pointset.width + 15

    @property
    def iframe_height(self):
        return self.pointset.height + 20

    @property
    def height(self):
        # image width
        return self.pointset.height

    @property
    def points(self):
        return self.pointset.points.all()

    @property
    def popup(self):
        """Show graphs big?
        """
        return self.request.GET.get('popup', 'false') == 'true'


class UploadedFileView(ViewContextMixin, TemplateView):
    template_name = 'lizard_levee/uploaded_files.html'

    @property
    def uploaded_files(self):
        return models.UploadedFile.objects.all()


class RiskTableView(ViewContextMixin, TemplateView):
    """Table with the Fugro-calculated risk data.

    Warning: there's a lot hardcoded in here.
    """
    template_name = "lizard_levee/risk_table.html"
    small = False

    def values_from_point_slugs(self, location, *slugs):
        points = [lizard_geodin.models.Point.objects.get(slug=slug)
                  for slug in slugs]  # Not as query to preserve order.
        values = ['%.1f' % float(point.last_value()) for point in points]
        return [location] + values

    @property
    def projects(self):
        results = [
            {'name': 'Veiligheidsfactoren',
             'headers': ['Segment',
                         'Macro',
                         'Micro',
                         ],
             'rows': [self.values_from_point_slugs(
                        'Een',
                        '0005110295MOS000',
                        '0005110297MOS000',
                        ),
                      self.values_from_point_slugs(
                        'Twee',
                        '0005110295MOS000',
                        '0005110297MOS000',
                        ),
                      self.values_from_point_slugs(
                        'Drie',
                        '0005110295MOS000',
                        '0005110297MOS000',
                        ),
                      self.values_from_point_slugs(
                        'Vier',
                        '0005110294MOS000',
                        '0005110296MOS000',
                        ),
                      self.values_from_point_slugs(
                        'Vijf',
                        '0005110294MOS000',
                        '0005110296MOS000',
                        ),
                      self.values_from_point_slugs(
                        'Zes',
                        '0005110294MOS000',
                        '0005110296MOS000',
                        ),
                      ]},
            ]

        return results
        # if not self.small:
        #     return results
        # for result in results:
        #     result['headers'] = result['headers'][:2]
        #     new_rows = []
        #     for row in result['rows']:
        #         new_row = row[:2]
        #     result['rows'] = new_rows
        # return results


# class SmallRiskTableView(RiskTableView):
#     small = True

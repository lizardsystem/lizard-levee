# Lots of copy/paste from lizard-riool, btw.  [reinout]
# from __future__ import unicode_literals  # DISABLED, mapnik dislikes it.
import os
import re

from django.conf import settings
from django.contrib.gis import geos
from django.db import connection
from lizard_map.workspace import WorkspaceItemAdapter
from lizard_map.models import WorkspaceItemError
from lizard_map.models import ICON_ORIGINALS
from lizard_map.symbol_manager import SymbolManager
import mapnik

from lizard_levee import models


# Colors from http://www.herethere.net/~samson/php/color_gradient/
CLASSES = (
    ('A', '0%-10%',   -0.01, 0.10, '00ff00'),
    ('B', '10%-25%',  0.10, 0.25, '669900'),
    ('C', '25%-50%',  0.25, 0.50, '996600'),
    ('D', '50%-75%',  0.50, 0.75, 'CC3200'),
    ('E', '75%-100%', 0.75, 1.01, 'ff0000'))


def get_class_boundaries(pct):
    "Return the class and its boundaries for a given fraction."
    for klasse, _, min_pct, max_pct, _ in CLASSES:
        if pct >= min_pct and pct < max_pct:
            return klasse, min_pct, max_pct


GENERATED_ICONS = os.path.join(settings.MEDIA_ROOT, 'generated_icons')
SYMBOL_MANAGER = SymbolManager(ICON_ORIGINALS, GENERATED_ICONS)
RIOOL_ICON = 'pixel.png'
RIOOL_ICON_LARGE = 'pixel16.png'

DATABASE = settings.DATABASES['default']
PARAMS = {
    'host': DATABASE['HOST'],
    'port': DATABASE['PORT'],
    'user': DATABASE['USER'],
    'password': DATABASE['PASSWORD'],
    'dbname': DATABASE['NAME'],
    # 'srid': models.SRID,
}


def html_to_mapnik(color):
    r, g, b = color[0:2], color[2:4], color[4:6]
    rr, gg, bb = int(r, 16), int(g, 16), int(b, 16)
    return rr / 255.0, gg / 255.0, bb / 255.0, 1.0


def default_database_params():
    """Get default database params. Use a copy of the dictionary
    because it is mutated by the functions that use it."""
    return PARAMS.copy()


class LeveeRisk(WorkspaceItemAdapter):
    # javascript_hover_handler = 'popup_hover_handler'

    def __init__(self, *args, **kwargs):
        super(LeveeRisk, self).__init__(*args, **kwargs)
        self.area_slug = self.layer_arguments['slug']
        try:
            self.area = models.Area.objects.get(
                slug=self.area_slug)
            self.segments = models.Segment.objects.filter(area=self.area)
        except models.Area.DoesNotExist:
            raise WorkspaceItemError(
                "Area %s doesn't exist." % self.area_slug)

    def layer(self, layer_ids=None, request=None):
        "Return Mapnik layers and styles."
        layers, styles = [], {}

        risk_style = mapnik.Style()

        for _, _, min_perc, max_perc, color in CLASSES:
            # r, g, b, a = html_to_mapnik(color)
            layout_rule = mapnik.Rule()
            symbol = mapnik.PolygonSymbolizer(mapnik.Color(str('#' + color)))
            layout_rule.symbols.append(symbol)
            layout_rule.filter = mapnik.Filter(
                str("[value] >= %s and [value] < %s" % (min_perc, max_perc)))
            risk_style.rules.append(layout_rule)

        styles["riskStyle"] = risk_style

        query = str("""(
            SELECT
                sg.risk AS value,
                sg.poly AS poly
            FROM
                lizard_levee_segment sg
            WHERE
                sg.area_id=%s
            ) AS data""" % (self.area.id,))
        params = default_database_params()
        params['table'] = query
        # params['geometry_field'] = 'poly'
        datasource = mapnik.PostGIS(**params)

        layer = mapnik.Layer('Levee risk')
        layer.datasource = datasource
        layer.styles.append("riskStyle")
        layers.append(layer)

        return layers, styles

    def legend(self, updates=None):
        legend = []
        for classname, classdesc, _, _, color in CLASSES:
            r, g, b, a = html_to_mapnik(color)

            icon = SYMBOL_MANAGER.get_symbol_transformed(
                RIOOL_ICON_LARGE, color=(r, g, b, a))

            legend.append({
                    'img_url': os.path.join(
                        settings.MEDIA_URL, 'generated_icons', icon),
                    'description': "klasse %s (%s)" % (classname, classdesc),
                    })
        return legend

    def extent(self, identifiers=None):
        "Return the extent in Google projection"
        cursor = connection.cursor()
        cursor.execute("""
            select ST_Extent(ST_Transform(poly, 900913))
            from lizard_levee_segment where area_id=%s
            """, [self.area.id])
        row = cursor.fetchone()
        box = re.compile('[(|\s|,|)]').split(row[0])[1:-1]
        return {
            'west': box[0], 'south': box[1],
            'east': box[2], 'north': box[3],
        }

    def search(self, x, y, radius=None):
        """We only use this for the mouse hover function; return the
        minimal amount of information necessary to show it."""

        pnt = geos.Point(x, y, srid=900913)
        points = (models.StoredGraph.objects.filter(rmb__id=self.id).
                  filter(xy__distance_lte=(pnt, radius)).
                  distance(pnt).
                  order_by('distance'))

        if not points:
            return []

        point = points[0]

        return [{
                'name': ('%.0f%% verloren berging' %
                         (point.flooded_percentage * 100,)),
                'stored_graph_id': point.pk,
                'distance': point.distance.m,
                }]

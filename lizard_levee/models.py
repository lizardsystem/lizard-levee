# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import json
import math

# from jsonfield import JSONField
from django.contrib.gis.geos import Polygon
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from lizard_wms.models import WMSSource
from sorl.thumbnail import ImageField

from lizard_geodin.models import Measurement
from lizard_geodin.models import Point

# Message Box

class MessageTag(models.Model):
    """The message tag discriminates between different categories.
    """
    name = models.CharField(max_length=40)
    tag = models.SlugField()
    html_color = models.CharField(max_length=10, default='black')

    def __unicode__(self):
        return self.name


class Message(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(MessageTag, null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)
    image_link = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-timestamp', )

    def __unicode__(self):
        return self.message

    def as_html(self):
        try:
            color = self.tags.all()[0].html_color
        except:
            color = 'red'  # alert color
        if self.timestamp:
            timestamp = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        else:
            timestamp = ''
        return '<font color="%s">%s %s</font>' % (
            color, timestamp, self.message)

    @property
    def image(self):
        """Return image_url except for some hardcoded exceptions..."""
        tags = ''.join([tag.tag for tag in self.tags.all()]).lower()
        if 'adviseur' in tags:
            return '/static_media/lizard_levee/nens_fugro.png'
        if 'proefleiding' in tags:
            return '/static_media/lizard_levee/tno.png'
        return self.image_url

    def tags_str(self):
        # Note: this string is really a unicode... Dangerous. [reinout]
        # Also: it is unused.
        return ', '.join([str(t) for t in self.tags.all()])


class MessageBox(models.Model):
    """ A message box can be displayed in the gui, the linked tags are
    displayed as checkboxes. The client requests the messages through
    an API and the state of the checkboxes.
    """
    title = models.CharField(
        _('title'),
        max_length=255,
        null=True,
        blank=True)
    tags = models.ManyToManyField(MessageTag, null=True, blank=True)
    slug = models.SlugField(
        _('slug'),
        help_text=_("Used in the URL."),
        null=True,
        blank=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lizard_levee_message_box', kwargs={'slug': self.slug})


# Image Map

class ImageMapGroup(models.Model):
    """
    Grouped image maps
    """
    title = models.CharField(
        _('title'),
        max_length=255,
        null=True,
        blank=True)
    index = models.IntegerField(default=100)

    class Meta:
        ordering = ('index', 'title', )

    def __unicode__(self):
        return self.title


class ImageMap(models.Model):
    """Define an image map with links: dwarsprofielen.

    Note that the image itself is not contained in this object. It can
    be a matplotlib graphic or anything that sits on the image_url.
    """

    title = models.CharField(
        _('title'),
        max_length=255,
        null=True,
        blank=True)
    slug = models.SlugField(
        _('slug'),
        help_text=_("Used in the URL."),
        null=True,
        blank=True)
    image_url = models.CharField(
        max_length=200,
        help_text=("Full /static_media path to background image. "
                   "See /levee/tools/imagemaps/ for a handy list."))
    image_width = models.IntegerField(default=800)
    image_height = models.IntegerField(default=250)
    image_scale = models.IntegerField(default=100, help_text="in percent") # used by ImageMapLink as well

    group = models.ForeignKey(
        ImageMapGroup,
        null=True,
        blank=True,
        help_text="Used for grouping the imagemap into a menu.")

    # Settings for automatially mapping points on an image
    auto_geo = models.ForeignKey(
        "ImageMapGeoPolygon", null=True, blank=True, help_text="Use this, or auto_geo_polygon")
    auto_geo_polygon = models.CharField(
        max_length=200,
        help_text="auto mapping: pairs of x,y coordinates: x0,y0,x1,y1,x2,y2,x3,y3,.... center is average coords",
        default="270000,570000,270000,580000,280000,580000,280000,570000", null=True, blank=True)
    auto_from_above = models.BooleanField(
        default=False, help_text="Either from above, or from the side")
    auto_geo_direction = models.FloatField(
        default=0.0,
        help_text=("Watch from which direction? In degrees. From east is 0, from north is 90, etc. "
                   "From side AND above (what is north)"))
    auto_scale_x = models.FloatField(default=1.0, help_text="topview: screen_x scale after rotate")
    auto_scale_y = models.FloatField(default=1.0, help_text="sideview: screen_x. topview: screen_y. scale after rotate")
    auto_scale_z = models.FloatField(default=100.0, help_text="sideview: screen_y. scale after rotate")

    auto_offset_x = models.FloatField(default=0.0, help_text="screen_x offset after scale")
    auto_offset_y = models.FloatField(default=0.0, help_text="screen_y offset after scale")

    auto_grouping_size = models.IntegerField(
        default=20,
        help_text="when should items be grouped together")

    class Meta:
        ordering = ('group', 'title', )

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lizard_levee_image_map',
                       kwargs={'slug': self.slug})

    @property
    def auto_poly(self):
        if self.auto_geo:
            return self.auto_geo.auto_poly
        elif self.auto_geo_polygon:
            coords = [float(i) for i in self.auto_geo_polygon.split(',')]  # alternated x, y, x, y..
            poly = [(coords[i*2], coords[i*2+1]) for i in range(len(coords)/2)]
            return poly

    @property
    def auto_center(self):
        """Return fixed rotation point
        """
        # poly = self.auto_poly
        # big_sum = reduce(lambda (x0, y0), (x1, y1): (x0+x1, y0+y1), poly)
        # return big_sum[0]/len(poly), big_sum[1]/len(poly)

        return 275000, 575000

    @property
    def auto_direction_radian(self):
        return self.auto_geo_direction / 360 * 2 * math.pi

    @property
    def image_scaled_width(self):
        return self.image_width * self.image_scale / 100


class ImageMapGeoPolygon(models.Model):
    """
    Define an area for ImageMap auto mapping
    """
    name = models.CharField(
        _('name'),
        max_length=255,
        null=True,
        blank=True)
    geo_polygon = models.CharField(
        max_length=200,
        help_text="auto mapping: pairs of x,y coordinates: x0,y0,x1,y1,x2,y2,x3,y3,.... center is average coords",
        default="270000,570000,270000,580000,280000,580000,280000,570000")

    @property
    def auto_poly(self):
        """Read out auto_geo_polygon as a list of 2-tuples"""
        coords = [float(i) for i in self.geo_polygon.split(',')]  # alternated x, y, x, y..
        poly = [(coords[i*2], coords[i*2+1]) for i in range(len(coords)/2)]
        return poly

    def __unicode__(self):
        return self.name


class ImageMapLinkPoint(models.Model):
    """
    An ordered Point in ImageMapLink
    """
    image_map_link = models.ForeignKey("ImageMapLink")
    point = models.ForeignKey(Point)
    index = models.IntegerField(default=100)

    class Meta:
        ordering = ('index', 'image_map_link', 'index')


class ImageMapLink(models.Model):
    """
    Each link, used in an image map
    """
    SHAPE_CHOICES = (
        ("polygon", "polygon"),
        ("rect", "rect"),
        ("circle", "circle"),)

    image_map = models.ForeignKey(ImageMap)
    image_map_index = models.IntegerField(default=100)

    # For hovers?
    title = models.CharField(
        _('title'),
        max_length=255,
        null=True,
        blank=True)
    # use for updating mechanisms to find objects back, objects
    # *should* be unique
    #identifier = models.CharField(max_length=80)

    # The linked object: take one of the two
    # measurement = models.ForeignKey(Measurement, null=True, blank=True)
    # segment = models.ForeignKey("Segment", null=True, blank=True)
    # ^^^ This isn't even used. Can it be zapped? [reinout], yes, measurement too [jack]

    # "Old" points: order is alphabetical. Popup of multipoints shows a list first.
    #point = models.ForeignKey(Point, null=True, blank=True)
    points = models.ManyToManyField(Point, null=True, blank=True)

    # Order of points must be user-defined. Popup shows all the graphs in order.
    ordered_points = models.ManyToManyField(
        Point, null=True, blank=True,
        through="ImageMapLinkPoint",
        related_name="ordered_points")

    target_url = models.TextField(
        null=True, blank=True,
        help_text="a link to be shown in popup")
    target_outline_color = models.CharField(
        max_length=20, null=True, blank=True,
        help_text="optional outline color for target_url")
    color_me = models.BooleanField(
        default=False,
        help_text="will be colored using first element of points or ordered_points")
    color_legend = models.ForeignKey(
        "ImageMapLegend", null=True, blank=True,
        help_text="provide legend, or use standard 0-1 legend"
        )

    #"polygon", "rect" or "circle"
    shape = models.CharField(choices=SHAPE_CHOICES, max_length=40)
    #dependent on shape,
    # circle: x, y, radius
    # polygon: x1, y1, x2, y2, x3, y3, ...
    # rect: x1, y1, x2, y2
    coords = models.CharField(max_length=200)

    class Meta:
        ordering = ('image_map', 'image_map_index', 'shape', 'coords', )

    # def linked_object(self):
    #     if self.ordered_points.all():
    #         return self.ordered_points.all()
    #     elif self.points.all():
    #         return self.points.all()
    #     else:
    #         return None

    def get_popup_url(self):
        extra_params = 'extra=True'
        if self.target_url:
            return self.target_url
        if self.ordered_points.all():
            if self.ordered_points.count() == 1:
                return self.ordered_points.all()[0].get_popup_url() + '?' + extra_params
            else:
                # The slugs must be in the correct order.
                return (
                    reverse('lizard_geodin_point_list') +
                    '?slug=' + '&slug='.join([
                            p.point.slug for p in
                            self.imagemaplinkpoint_set.all().order_by('index')]) +
                    '&' + extra_params
                    )
        if self.points.all():
            if self.points.count() == 1:
                return self.points.all()[0].get_popup_url() + '?' + extra_params
            else:
                return (
                    reverse('lizard_geodin_point_list') +
                    '?slug=' + '&slug='.join([p.slug for p in self.points.all()]) +
                    '&' + extra_params
                    )

        return ""

    @property
    def display_title(self):
        add_to_title = ''
        if self.points:
            if self.points.count() == 1:
                try:
                    add_to_title = ' (%s)' % self.points.all()[0].last_value()
                except:
                    add_to_title = ''
                    # import traceback, sys
                    # traceback.print_exc(file=sys.stdout)
                    # exc_type, exc_value, exc_traceback = sys.exc_info()
                    # print "*** print_tb:"
                    # traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
                    # print "*** print_exception:"
                    # traceback.print_exception(exc_type, exc_value, exc_traceback,
                    #                           limit=2, file=sys.stdout)
        if self.ordered_points:
            try:
                # show data of first point
                if self.color_me:
                    add_to_title = ' (%s)' % self.ordered_points.all()[0].last_value()
            except:
                pass
        if self.title:
            return self.title + add_to_title
        else:
            return str(self.linked_object()) + add_to_title

    @property
    def coords_scaled(self):
        """
        Scaled by ImageMap.image_scale
        """
        scale = self.image_map.image_scale
        result = [int(c) * scale / 100 for c in self.coords.split(',')]
        return ','.join([str(r) for r in result])

    def __unicode__(self):
        return '%s %s %s' % (self.image_map, self.shape, self.coords)


class ImageMapLegend(models.Model):
    """
    For use in ImageMapMapView
    """
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return '%s' % self.name


class ImageMapLegendSection(models.Model):
    """
    """
    image_map_legend = models.ForeignKey("ImageMapLegend")
    value_lower = models.FloatField(
        null=True, blank=True, help_text="leave empty is open boundary")
    value_upper = models.FloatField(
        null=True, blank=True, help_text="leave empty is open boundary")
    html_color = models.CharField(max_length=20, default="#ff0000")

    class Meta:
        ordering = ('value_lower', )

    def __unicode__(self):
        return "%s, %r %r %s" % (self.image_map_legend, self.value_lower, self.value_upper, self.html_color)


class InformationPointer(models.Model):
    """Information pointer, like failure mechanisms."""
    title = models.CharField(
        _('title'),
        max_length=255,
        null=True,
        blank=True)
    slug = models.SlugField(
        _('slug'),
        help_text=_("Used in the URL."),
        null=True,
        blank=True)
    description = models.TextField(
        _('description'),
        null=True,
        blank=True)
    more_url = models.URLField(
        _('more url'),
        help_text=_("URL with more explanation. If not available, the "
                    "link points at the full-size image (as fallback)."),
        null=True,
        blank=True)
    image = ImageField(
        _('image'),
        upload_to='levee_information_pointer',
        help_text=_("Scaled automatically."),
        null=True,
        blank=True)

    class Meta:
        verbose_name = _('information pointer')
        verbose_name_plural = _('information pointers')

    def __unicode__(self):
        return self.title

    def href(self):
        """Return more_url; fallback is the full image url."""
        if self.more_url:
            return self.more_url
        return self.image.url


class Link(models.Model):
    """URL pointing at another website."""
    title = models.CharField(
        _('title'),
        max_length=255,
        null=True,
        blank=True)
    description = models.TextField(
        _('description'),
        null=True,
        blank=True)
    url = models.URLField(
        _('URL'),
        null=True,
        blank=True)

    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _('links')
        ordering = ('title', )

    def __unicode__(self):
        return '%s (%s)' % (self.title, self.url)


class LinkSet(models.Model):
    """A bunch of links"""
    name = models.CharField(
        _('name'),
        max_length=255,
        null=True,
        blank=True)
    slug = models.SlugField(
        _('slug'),
        help_text=_("Used in the URL."),
        null=True,
        blank=True)
    links = models.ManyToManyField(Link, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Area(models.Model):
    """An area is a collection of levees.

    Basically it is a wrapper around a lizard-geodin project.
    """
    name = models.CharField(
        _('name'),
        max_length=255,
        null=True,
        blank=True)
    slug = models.SlugField(
        _('slug'),
        help_text=_("Used in the URL."),
        null=True,
        blank=True)
    description = models.TextField(
        _('description'),
        help_text=_(
            "Just plain text. Shown as a short description in the sidebar."),
        null=True,
        blank=True)
    wms_layers = models.ManyToManyField(
        WMSSource,
        verbose_name=_('WMS layers'),
        help_text=_("Pointer at WMS sources that visualize us on the map."),
        null=True,
        blank=True,
        )
    information_pointers = models.ManyToManyField(
        InformationPointer,
        verbose_name=_('information pointers'),
        help_text=_("Shown on the overview page as background information."),
        null=True,
        blank=True,
        )
    links = models.ManyToManyField(
        Link,
        verbose_name=_('links'),
        help_text=_("Links to relevant other websites."),
        null=True,
        blank=True,
        )
    cross_section_image = ImageField(
        _('cross section image'),
        upload_to='levee_cross_section',
        help_text=_("Scaled automatically."),
        null=True,
        blank=True)
    longitudinal_cross_section_image = ImageField(
        _('longitudinal cross section image'),
        upload_to='levee_longitudinal_section',
        help_text=_("Scaled automatically."),
        null=True,
        blank=True)
    segments_jsonfile = models.FileField(
        _('levee segments json file'),
        upload_to='levee_segments',
        null=True,
        blank=True)

    class Meta:
        verbose_name = _('area')
        verbose_name_plural = _('areas')

    def get_absolute_url(self):
        return reverse('lizard_levee_burgomaster',
                       kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Area, self).save(*args, **kwargs)
        if not self.segments_jsonfile:
            return
        the_json = json.loads(self.segments_jsonfile.read())
        features = the_json.get('features')
        if features is None:
            return
        for feature in features:
            id = feature['id']
            poly_coordinates = feature['geometry']['coordinates'][0]
            segment, created = Segment.objects.get_or_create(area=self,
                                                             segment_id=id)
            segment.poly = Polygon(poly_coordinates, srid=28992)
            segment.save()


class Segment(models.Model):
    """Segment of the levee."""
    poly = models.PolygonField(
        null=True,
        blank=True)
    area = models.ForeignKey(
        'Area',
        null=True,
        blank=True,
        related_name='segments')
    segment_id = models.IntegerField()  # Not the same as self.id!
    risk = models.FloatField(
        _('risk'),
        default=0)
    objects = models.GeoManager()

    class Meta:
        verbose_name = _('levee segment')
        verbose_name_plural = _('levee segments')

    def __unicode__(self):
        return unicode(self.segment_id)


class PointSet(models.Model):
    """
    A set of points, for easy configuring and displaying
    """
    name = models.CharField(
        _('name'),
        max_length=255)
    slug = models.SlugField(
        _('slug'),
        help_text=_("Used in the URL."),
        null=True,
        blank=True)
    width = models.IntegerField(default=500)
    height = models.IntegerField(default=100)
    points = models.ManyToManyField(Point, null=True, blank=True)

    index = models.IntegerField(default=100)

    class Meta:
        ordering = ('index', )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("lizard_levee_pointset", kwargs={'slug': self.slug})


class UploadedFile(models.Model):
    name = models.CharField(
        _('name'),
        max_length=255)
    timestamp = models.DateTimeField(blank=True, null=True)
    uploaded_file = models.FileField(upload_to='docs', blank=True, null=True)

    def __unicode__(self):
        return self.name

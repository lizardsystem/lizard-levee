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
    # TODO: change to 'last_modified' and add 'real' timestamp
    timestamp = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(MessageTag, null=True, blank=True)

    class Meta:
        ordering = ('timestamp', )

    def __unicode__(self):
        return self.message

    def as_html(self):
        try:
            color = self.tags.all()[0].html_color
        except:
            color = 'red'  # alert color
        return '<font color="%s">%s: %s</font>' % (
            color, self.timestamp.strftime('%Y-%m-%d %H:%M:%S'), self.message)

    def tags_str(self):
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
    image_url = models.CharField(max_length=200)
    image_width = models.IntegerField(default=300)
    image_height = models.IntegerField(default=300)

    group = models.ForeignKey(
        ImageMapGroup, null=True, blank=True)

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
        """Read out auto_geo_polygon as a list of 2-tuples"""
        coords = [float(i) for i in self.auto_geo_polygon.split(',')]  # alternated x, y, x, y..
        poly = [(coords[i*2], coords[i*2+1]) for i in range(len(coords)/2)]
        return poly

    @property
    def auto_poly(self):
        if self.auto_geo:
            return self.auto_geo.auto_poly
        else:
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

        return 275000,575000

    @property
    def auto_direction_radian(self):
        return self.auto_geo_direction / 360 * 2 * math.pi


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
    measurement = models.ForeignKey(Measurement, null=True, blank=True)
    segment = models.ForeignKey("Segment", null=True, blank=True)
    #point = models.ForeignKey(Point, null=True, blank=True)
    points = models.ManyToManyField(Point, null=True, blank=True)
    #destination_url = models.TextField()  # take get_absolute_url from measurement

    #"polygon", "rect" or "circle"
    shape = models.CharField(choices=SHAPE_CHOICES, max_length=40)
    #dependent on shape,
    # circle: x, y, radius
    # polygon: x1, y1, x2, y2, x3, y3, ...
    # rect: x1, y1, x2, y2
    coords = models.CharField(max_length=200)

    class Meta:
        ordering = ('image_map_index', )

    def linked_object(self):
        if self.points.all():
            return self.points.all()
        elif self.measurement:
            return self.measurement
        else:
            return self.segment

    def get_popup_url(self):
        if not self.points.all():
            return self.linked_object().get_popup_url()
        else:
            if self.points.count() == 1:
                return self.points.all()[0].get_popup_url()
            else:
                return (
                    reverse('lizard_geodin_point_list')+
                    '?slug='+'&slug='.join([p.slug for p in self.points.all()]))

    @property
    def display_title(self):
        if self.title:
            return self.title
        else:
            return str(self.linked_object())


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

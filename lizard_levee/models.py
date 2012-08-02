# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals
import json

# from jsonfield import JSONField
from django.contrib.gis.geos import Polygon
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from lizard_wms.models import WMSSource
from sorl.thumbnail import ImageField


class ImageMapGroup(models.Model):
    """
    Grouped image maps
    """
    title = models.CharField(
        _('title'),
        max_length=255,
        null=True,
        blank=True)

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

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lizard_levee_image_map',
                       kwargs={'slug': self.slug})


class ImageMapLink(models.Model):
    """
    Each link, used in an image map
    """
    SHAPE_CHOICES = (
        ("polygon", "polygon"),
        ("rect", "rect"),
        ("circle", "circle"),)

    image_map = models.ForeignKey(ImageMap)
    # For hovers?
    title = models.CharField(
        _('title'),
        max_length=255,
        null=True,
        blank=True)
    # use for updating mechanisms to find objects back, objects
    # *should* be unique
    identifier = models.CharField(max_length=80)
    destination_url = models.TextField()

    #"polygon", "rect" or "circle"
    shape = models.CharField(choices=SHAPE_CHOICES, max_length=40)
    #dependent on shape,
    # circle: x, y, radius
    # polygon: x1, y1, x2, y2, x3, y3, ...
    # rect: x1, y1, x2, y2
    coords = models.CharField(max_length=200)


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

    def __unicode__(self):
        return '%s (%s)' % (self.title, self.url)


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


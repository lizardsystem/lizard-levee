# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from lizard_wms.models import WMSSource
from sorl.thumbnail import ImageField


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

    class Meta:
        verbose_name = _('area')
        verbose_name_plural = _('areas')

    def get_absolute_url(self):
        return reverse('lizard_levee_burgomaster',
                       kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.name

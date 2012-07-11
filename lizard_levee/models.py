# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from lizard_wms.models import WMSSource
from sorl.thumbnail import ImageField


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

    class Meta:
        verbose_name = _('area')
        verbose_name_plural = _('areas')

    def get_absolute_url(self):
        return reverse('lizard_levee_burgomaster',
                       kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.name


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
    area = models.ForeignKey(
        Area,
        null=True,
        blank=True,
        related_name='information_pointers')
    highlighted = models.BooleanField(
        _('highlighted'),
        default=False)
    description = models.TextField(
        _('description'),
        null=True,
        blank=True)
    more_url = models.URLField(
        _('more url'),
        help_text=_("URL with more explanation."),
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

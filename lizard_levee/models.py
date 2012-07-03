# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


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
        help_text=_("Used in the url of the area."),
        null=True,
        blank=True)

    def get_absolute_url(self):
        return reverse('lizard_levee_burgomaster',
                       kwargs={'slug': self.slug})


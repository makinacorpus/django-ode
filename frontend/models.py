# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CarouselImage(models.Model):
    class Meta:
        verbose_name = _('Image du carousel')
        verbose_name_plural = _('Images du carousel')
        ordering = ('position', 'name')

    name = models.CharField(_('nom'), max_length=255)
    image = models.ImageField(_('image'), upload_to='carousel_uploads')
    position = models.PositiveIntegerField(
        _('position'), default=1,
        help_text="La position de l'image dans la séquence")

    def url(self):
        return self.image.path
        return '/media/carousel_uploads/' + self.filename

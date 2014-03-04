# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import CarouselImage


class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('position', 'name')
    list_display_links = ('name',)
    list_editable = ('position',)


admin.site.register(CarouselImage, CarouselImageAdmin)

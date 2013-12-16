# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db.models import TextField

from dashboard.models import Event, Source, Location, Tag
from dashboard.models import CategoryAssociation, TagAssociation

from ckeditor.widgets import CKEditorWidget


class LocationInline(admin.StackedInline):
    model = Location
    fk_name = "event"
    fields = ('name', 'address', 'post_code', 'town', 'country', 'capacity')
    max_num = 1


class TagInline(admin.StackedInline):
    exclude = ('id', )
    model = TagAssociation
    extra = 1


class CategoryInline(admin.StackedInline):
    exclude = ('id', )
    model = CategoryAssociation
    extra = 1


class EventAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )
    list_display = ('title', )
    fieldsets = (
        (None, {
            'fields': ('id', 'title', 'description', 'start_time', 'end_time',
                       'publication_start',
                       'publication_end', 'performers')
        }),
        (_('Organisateur'), {
            'fields': ('firstname', 'lastname', 'email', 'telephone'),
        }),
        (_(u'Infos générales événement'), {
            'fields': ('price_information', 'target', ),
        }),
        (_('Contact presse'), {
            'fields': ('press_contact_name', 'press_contact_email',
                       'press_contact_phone_number'),
        }),
        (_('Contact billeterie'), {
            'fields': ('ticket_contact_name', 'ticket_contact_email',
                       'ticket_contact_phone_number'),
        }),
    )
    inlines = [
        LocationInline,
        TagInline,
        CategoryInline,
    ]


class SourceAdmin(admin.ModelAdmin):
    list_display = ('url', )
    fields = ('url', )


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )
    fields = ('name', )


class FlatPageCustom(FlatPageAdmin):
    formfield_overrides = {
        TextField: {'widget': CKEditorWidget}
    }


admin.site.register(Event, EventAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageCustom)

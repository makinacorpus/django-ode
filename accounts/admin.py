# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from accounts.models import User
from accounts.models import Organization


class UserAdmin(admin.ModelAdmin):
    fields = ('is_active', 'first_name', 'last_name', 'username', 'email',
              'phone_number', 'organization')


class UserInline(admin.StackedInline):
    model = User
    fk_name = "organization"
    fields = ('first_name', 'last_name', 'username', 'email', 'phone_number', )


class OrganizationAdmin(admin.ModelAdmin):
    fieldsets = (
        (_(u'Image'), {
            'fields': ('picture',),
        }),
        (_(u'Fournisseur'), {
            'fields': ('is_provider', 'is_host', 'is_performer', 'is_creator'),
        }),
        (_(u'Réutilisateur'), {
            'fields': ('is_consumer', 'is_media', 'is_website',
                       'is_mobile_app', 'is_other'),
        }),
        (_(u'Infos Structure'), {
            'fields': ('type', 'name', 'address', 'post_code', 'town', 'url',
                       'activity_field'),
        }),
        (_(u'Infos générales événement'), {
            'fields': ('price_information', 'audience', 'capacity'),
        }),
    )
    inlines = [
        UserInline,
    ]


admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)

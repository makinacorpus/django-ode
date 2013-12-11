from django.contrib import admin
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
        ('Image', {
            'fields': ('picture',),
        }),
        ('Fournisseur', {
            'fields': ('is_provider', 'is_host', 'is_performer', 'is_creator'),
        }),
        ('Réutilisateur', {
            'fields': ('is_consumer', 'is_media', 'is_website',
                       'is_mobile_app', 'is_other'),
        }),
        ('Infos Structure', {
            'fields': ('type', 'name', 'address', 'post_code', 'town', 'url',
                       'activity_field'),
        }),
        ('Infos générales événement', {
            'fields': ('price_information', 'audience', 'capacity'),
        }),
    )
    inlines = [
        UserInline,
    ]


admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)

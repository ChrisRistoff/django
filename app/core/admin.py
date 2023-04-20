''' django admin customizing '''

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
from django.utils.translation import gettext as _


class UserAdmin(BaseUserAdmin):
    '''customize the admin page for the user model'''

    # change the order of the fields in the admin page for the user models
    # the fields are displayed in the order they are listed
    # ordering is built in to the admin page
    ordering = ['id']
    list_display = ['email', 'name']

    # add the fieldsets to the admin page for the user models.
    # fieldsets is built in to the admin page and is used to group
    # the fields in the admin page for the user models
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            # the _() is used to translate the string to the language
            # of the user using the site and is built in to django
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    )
            }
        ),

        (_("important dates"), {'fields': ('last_login',)}),
    )

    # readonly_fields is built in to the admin page and is used to
    # make the fields read only in the admin page for the user models
    readonly_fields = ('last_login',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
                )
        }),

    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
# convert string to readeable text, so it gets
# passed through the translation engine

from . import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    # order by id, list by email and name
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    # we basically define the sections for the
    # field sets in our change and create page.
    # each () is a section, inside, we write the title

    # just note the comma here
    # after name, if you're just providing one field then you
    # need to make sure you add
    # this comma because otherwise it thinks this is just a
    # string and it won't work.

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Tag)
# supports the basic create, read, update and delete
# functions in the admin panel
admin.site.register(models.Ingredient)
admin.site.register(models.Recipe)
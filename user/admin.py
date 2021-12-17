from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


class UserAdmin(BaseUserAdmin):
    list_display = ( 'email',
                    'fio',
                    'phone',
                    'own_ref_code',
                    'used_ref_code',
                    'balance',
                    'ref_bonuses',
                    'total_spend',
                    )
    ordering = ('id',)
    search_fields = ('email', 'fio', 'phone', 'own_ref_code', 'used_ref_code',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info',
         {'fields': (
                    'fio',
                    'phone',
                    'own_ref_code',
                    'used_ref_code',
                    'balance',
                    'ref_bonuses',
                    'total_spend',

         )}
         ),
        ('Permissions', {'fields': ('is_staff', 'is_superuser',)}),)

admin.site.register(User,UserAdmin)
admin.site.register(UserRefferalFirstLine)
admin.site.register(UserRefferalSecondLine)
admin.site.register(UserRefferalThirdLine)

from django.contrib import admin
from .models import *


class ItemAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'name', 'price']
    list_filter = ('category',)
    search_fields = ('name',)
    class Meta:
        model = Item

admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
admin.site.register(Complect)



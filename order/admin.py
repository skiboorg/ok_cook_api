from django.contrib import admin
from .models import *

class OrderItemInline (admin.TabularInline):
    model = OrderItem
    readonly_fields = ('image_tag','item','amount',)
    extra = 0


class OrderCitySectorInline (admin.TabularInline):
    model = OrderCitySector
    extra = 0

class OrderCityAdmin(admin.ModelAdmin):
    inlines = [OrderCitySectorInline]

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'code',
                    'user',
                    'created_at',
                    'is_pay',
                    'is_done',
                    )
    search_fields = ('user__email', 'code', )
    list_filter = ('is_pay','is_done',)
    inlines = [OrderItemInline]

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(OrderCity, OrderCityAdmin)

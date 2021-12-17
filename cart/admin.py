from django.contrib import admin
from .models import *


class ItemInline (admin.TabularInline):
    model = CartComplectItem
    extra = 0

class ComplectAdmin(admin.ModelAdmin):
    inlines = [ItemInline]

class CartComplectInline (admin.TabularInline):
    model = CartComplect
    extra = 0

class CartAdmin(admin.ModelAdmin):
    inlines = [CartComplectInline]

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(CartComplect,ComplectAdmin)
admin.site.register(CartComplectItem)
# Register your models here.

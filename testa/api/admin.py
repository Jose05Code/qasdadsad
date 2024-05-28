from django.contrib import admin
from . models import Item, InventoryItem, SalesItem, OfferItem, Location

class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'gtin']

class ItemRelatedAdmin(admin.ModelAdmin):
    list_display = ['item_name']

    def item_name(self, obj):
        return obj.item.name
    item_name.short_description = 'Item Name'  # Sets column header in admin site

admin.site.register(Item, ItemAdmin)
admin.site.register(InventoryItem, ItemRelatedAdmin)
admin.site.register(SalesItem, ItemRelatedAdmin)
admin.site.register(OfferItem, ItemRelatedAdmin)
admin.site.register(Location, ItemRelatedAdmin)
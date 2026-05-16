from django.contrib import admin
from .models import BorrowRequest, Item, Category

admin.site.site_header = 'MRIIC Research Lab Inventory'
admin.site.site_title = 'MRIIC Staff Admin'
admin.site.index_title = 'Staff Administration'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_qty', 'featured')
    list_filter = ('featured', 'category')
    search_fields = ('name', 'item_desc')
    filter_horizontal = ('category',)


@admin.register(BorrowRequest)
class BorrowRequestAdmin(admin.ModelAdmin):
    list_display = ('item', 'requester_name', 'requester_email', 'quantity', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('item__name', 'requester_name', 'requester_email')
    readonly_fields = ('created_at', 'updated_at')

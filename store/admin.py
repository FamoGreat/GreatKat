from django.contrib import admin
from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date','is_available')
    list_display_links = ('product_name',)
    prepopulated_fields = {'slug': ('product_name',)}
    list_editable = ('price', 'stock', 'is_available')
    list_filter = ('category',)
    search_fields = ('product_name', 'category')


admin.site.register(Product, ProductAdmin)
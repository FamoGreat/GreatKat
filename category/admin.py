from django.contrib import admin
from .models import Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug', 'description', 'category_image')
    search_fields = ('category_name', 'slug')
    list_filter = ('category_name',)


admin.site.register(Category, CategoryAdmin)


from django.contrib import admin
from shop.models import Category,Product,SlideImage
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name','slug')
	prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name','slug','price','available','created','updated')
	list_filter = ['available','created','updated']
	list_editable = ['price','available']
	prepopulated_fields = {'slug':('name',)}

@admin.register(SlideImage)
class ImagesAdmin(admin.ModelAdmin):
	list_display = ('name','product')
	search_fields = ('name',)

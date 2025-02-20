from django.contrib import admin
from .models import Category
from .models import Product
# from .models import *

# to alter the lists in the admin page
class CategoryAdmin (admin.ModelAdmin):
    list_display = ('name', 'description')

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
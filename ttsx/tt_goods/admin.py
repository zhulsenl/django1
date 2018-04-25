from django.contrib import admin

# Register your models here.
from .models import GoodsCategory,Goods
admin.site.register(GoodsCategory)
admin.site.register(Goods)
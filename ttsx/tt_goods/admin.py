from django.contrib import admin
from django.core.cache import cache
# Register your models here.
from .models import GoodsCategory,Goods,IndexGoodsBanner,IndexCategoryGoodsBanner,IndexPromotionBanner
# from utils import gen_html
from utils import celery_tasks

class BaseAdmin(admin.ModelAdmin):
    # 保存模型时，会调用这个方法
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        celery_tasks.gen_index.delay()
        # 删除首页数据的缓存
        cache.delete('index_data')
    # 删除模型时，会调用这个方法
    def delete_model(self, request, obj):
        # obj.isDelete = True
        # obj.save()
        # 物理删除
        # obj.delete()
        super().delete_model(request,obj)
        # 数据被删除时，需要重新生成静态首页
        celery_tasks.gen_index.delay()
        # 删除首页数据的缓存
        cache.delete('index_data')


class GoodsCategoryAdmin(BaseAdmin):
    list_display = ['id', 'name', 'logo']
    # # 保存模型时，会调用这个方法
    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     gen_html.gen_index()
    #
    # # 删除模型时，会调用这个方法
    # def delete_model(self, request, obj):
    #     # obj.isDelete = True
    #     # obj.save()
    #     # 物理删除
    #     # obj.delete()
    #     super().delete_model(request,obj)
    #     # 数据被删除时，需要重新生成静态首页
    #     gen_html.gen_index()

class IndexGoodsBannerAdmin(BaseAdmin):
    list_display = ['sku', 'image', 'index']


class IndexCategoryGoodsBannerAdmin(BaseAdmin):
    list_display = ['category', 'sku', 'display_type', 'index']

class IndexPromotionBannerAdmin(BaseAdmin):
    list_display = ['name', 'url', 'image', 'index']



admin.site.register(GoodsCategory, GoodsCategoryAdmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(IndexCategoryGoodsBanner, IndexCategoryGoodsBannerAdmin)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)
admin.site.register(Goods)
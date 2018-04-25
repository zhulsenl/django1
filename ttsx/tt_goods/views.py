from django.shortcuts import render
from .models import *
# Create your views here.
def index(request):

    # 1.查询所有的分类
    category_list = GoodsCategory.objects.filter(isDelete=False)
    # 2.查询首页推荐商品
    index_goods_banner_list = IndexGoodsBanner.objects.all().order_by('index')
    # 3.查询首页广告
    index_promotion_list = IndexPromotionBanner.objects.all().order_by('index')

    # 4.遍历分类，查询每个分类的标题推荐、图片推荐
    # 在分类对象上增加类属性标题推荐列表，图片推荐列表
    for category in category_list:
        # 查询指定分类的标题推荐商品
        category.title_list= IndexCategoryGoodsBanner.objects.filter(category=category,display_type=0).order_by('index')

        # 查询指定分类的标题推荐商品
        category.image_list = IndexCategoryGoodsBanner.objects.filter(category=category, display_type=1).order_by(
            'index')

    context = {
            'category_list':category_list,
            'index_goods_banner_list':index_goods_banner_list,
            'index_promotion_list': index_promotion_list,
     }
    return render(request, 'index.html', context)
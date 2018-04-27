from django.shortcuts import render
from .models import *
from django.conf import settings
import os
from django.core.cache import cache
from django.http import Http404

#在django中操作redis,使用django_redis，不用编写原生的python代码
from django_redis import get_redis_connection



# Create your views here.
def index(request):
    # 从缓存中读取数据，如果没读到，则进行查询，然后保存
    context = cache.get('index_data')
    if context is None:
        print('-----------no cache')
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
        cache.set('index_data',context)


    response = render(request, 'index.html', context)
    # 响应体
    # html_str = response.content.decode()
    # # 写文件
    # with open(os.path.join(settings.BASE_DIR,'static/index.html'), 'w') as html_index:
    #     html_index.write(html_str)
    return response


def detail(request, sku_id):
    try:
        sku = GoodsSKU.objects.get(pk=sku_id)
    except:
        return Http404

    # 查询所有分类信息
    category_list = GoodsCategory.objects.filter(isDelete=False)


    # 查询当前商品所在分类，最新的两个商品
    # 根据当前商品找到对应的分类对象
    category_curr = sku.category
    # 查找指定类对应的所有的商品
    new_list = category_curr.goodssku_set.all().order_by('-id')[0:2]

    # 最近浏览,判断用户是否登录
    if request.user.is_authenticated():
        browser_key = 'browser%d'%request.user.id
        # 创建redis服务器的连接，默认使用settings-->caches中的配置
        redis_client = get_redis_connection()

        # 如果当前商品编号已经存在了，则删除
        redis_client.lrem(browser_key, 0, sku_id)
        # 记录商品的编号
        redis_client.lpush(browser_key, sku_id)
        # 如果总个数超过5个，则删除最右侧的一个
        if redis_client.llen(browser_key)>5:
            redis_client.rpop(browser_key)

    # 查询陈列数据
    # 1.根据sku找spu
    spu = sku.goods
    # 2.根据spu找所有的sku
    sku_list = spu.goodssku_set.all()


    context = {

        'title':'商品详情介绍',
        'sku':sku,
        'category_list':category_list,
        'new_list':new_list,
        'sku_list':sku_list

    }
    return render(request, 'detail.html', context)
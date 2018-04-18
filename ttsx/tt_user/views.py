from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.views.generic import View
import re
from .models import User
# 引入django发送邮件的函数
from django.core.mail import send_mail
from django.conf import settings

# 对json数据进行有时效性的加密
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from utils import celery_tasks

# Create your views here.
#

# 接收get方式的请求,用于展示注册页面
# 接收post方式的请求,用于注册处理

# def register(request):
#     if request.method == 'GET':
#         return render(request, 'register.html')
#     elif request.method == 'post':
#         return  HttpResponse('ok')
# 类试图，根据请求方式，查找对应的处理函数
class RegisterView(View):
    """类试图：处理注册"""
    def get(self, request):
        """处理GET请求，返回注册页面"""
        return render(request, 'register.html')

    def post(self, request):
        """处理POST请求，处理注册逻辑"""
        # return HttpResponse('ok')
#     1.接收所有请求的数据
        dict1 = request.POST # 为什么用字典？？？
        user_name = dict1.get('user_name')
        pwd = dict1.get('pwd')
        cpwd = dict1.get('cpwd')
        email = dict1.get('email')
        allow = dict1.get('allow')
        print(allow)
        # 判断是否接受协议
        if allow == None:
            return render(request, 'register.html')

        # 相同的问题，不同的方法
        # if allow != '1':
        #     return render(request, 'register.html')




#     2.验证数据的完整性all([]):迭代列表，判断每个元素的值，如果有false，则为false
        if not all([user_name,pwd,cpwd,email]):
            return render(request,'register.html')





#     3.验证数据的正确性
#      是否接受协议
#      邮箱格式是否正确
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html')
#      密码是否一致
        if pwd != cpwd:
            return render(request, 'register.html')
#      用户名是否存在
        if User.objects.filter(username=user_name).count()>=1:
            return render(request, 'register.html')
#       4.保存用户对象 create_user会自动加密
#        默认用户创建为激活状态，需要手动将其设置为非激活
        #  user = User()
#
#         user.save()
        user = User.objects.create_user(user_name, email, pwd)
        user.is_active = False
        user.save()
# 5.提示：请到邮箱中激活

        return HttpResponse('请到邮箱中激活')

def user_name(request):
    # 接收用户名
    uname = request.GET.get('uname')
    # 查询判断是否存在
    result = User.objects.filter(username=uname).count()
    # 返回提交信息
    return JsonResponse({'result':result})


def send_active_mail(request):
#     # 查找邮箱
#     user = User.objects.get(pk=3)
#     # user.id
#     # user.email
#     # 发邮件
#     # 定义邮件内容
#
#     # 加逻辑：对用户编号进行加密
#     user_dict = {'user_id':user.id}
#     serializer = Serializer(settings.SECRET_KEY,expires_in=10 )
#     str1 = serializer.dumps(user_dict).decode()
#
#
#     # 指定用户id
#     mail_body = '<a href="http://127.0.0.1:8000/user/active/%s">点击激活</a>'%str1
#     # 参数2表示message，内容是纯文本
#     # 参数html_message，内容是html
#     # 如果内容是html,则将第二个参数设置为’‘。再设置html_message参数
#     send_mail('用户激活','',settings.EMAIL_FROM,[user.email],html_message=mail_body)
#     # 提示
#     return HttpResponse('请到邮箱中激活')

    # delay()将celery的任务加到队列中

    user = User.objects.get(pk=3)
    celery_tasks.send_active_mail.delay(user.email, user.id)
    return HttpResponse('请到邮箱中激活')




def user_active(request, user_str):
    # 1.从地址中接收用户编号(见url配置)

    # 加逻辑，解密

    serializer = Serializer(settings.SECRET_KEY)
    # 如果时间超过规定的时间，会抛出异常
    try:
        user_dict = serializer.loads(user_str)
        user_id = user_dict.get('user_id')
        print('------------%s'%user_id)
    except:
        return HttpResponse('地址无效')
    # 2.根据编号查询用户对象
    user = User.objects.get(pk=user_id)
    # 3.修改is_active属性为True
    user.is_active = True
    user.save()
    # 4.提示：转到登录页 redirect 是自动跳转的意思
    return redirect('/user/login')


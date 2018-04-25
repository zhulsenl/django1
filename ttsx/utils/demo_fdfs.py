from fdfs_client.client import Fdfs_client
from django.conf import settings

# 根据配置文件，创建fdfs的客户端，通过这个对象上传文件到fdfs。
client = Fdfs_client(conf_path='/etc/fdfs/client.conf')

# 调用方法上传文件
result = client.upload_by_file('/home/python/Desktop/1.png')

print(result)
"""
{'Remote file_id': 'group1/M00/00/00/wKgoglrfHb6AYsGxAAGUgDbxZ8U561.png',
'Uploaded size': '101.00KB', 'Group name': 'group1', 'Status': 'Upload successed.',
'Storage IP': '192.168.40.130', 'Local file name': '/home/python/Desktop/1.png'}
"""
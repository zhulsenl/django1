from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.conf import settings


class FdfsStorage(Storage):
    # 只要进行文件保存，
    # 保存成功后，需要返回文件的名称，用于保存到表中
    def save(self, name, content, max_length=None):
        try:
            # 根据配置文件，创建fdfs的客户端，通过这个对象上传文件到fdfs。
            client = Fdfs_client(conf_path=settings.FDFS_CLIENT)

            # client获取文件内容
            file_data = content.read()

            # content表示上传文件的内容，已bytes类型进行上传。
            result = client.upload_by_buffer(file_data)
            if result.get('Status') == 'Upload successed.':
                # 上传成功后，返回文件的名称
                return result.get('Remote file_id')
            else:
                return ''
        except:
            return ''

        # print(result)
        """
        {'Remote file_id': 'group1/M00/00/00/wKgoglrfHb6AYsGxAAGUgDbxZ8U561.png',
        'Uploaded size': '101.00KB', 'Group name': 'group1', 'Status': 'Upload successed.',
        'Storage IP': '192.168.40.130', 'Local file name': '/home/python/Desktop/1.png'}
        """

    def url(self, name):
        return settings.FDFS_URL + name
__author__ = 'Hk4Fun'
__date__ = '2018/1/9 2:23'

from BiHu import settings
import os, uuid, datetime


# 目录创建
def upload_generation_dir(dir_name):
    today = datetime.datetime.today()
    for date in [today.year, today.month, today.day]:
        dir_name = os.path.join(dir_name, str(date))
    relative_path = dir_name
    path = os.path.join(settings.MEDIA_ROOT, dir_name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path, relative_path


# 图片上传
def image_upload(files, dir_name):
    # 允许上传文件类型
    allow_suffix = ['jpg', 'png', 'jpeg', 'gif', 'bmp']
    file_suffix = files.name.split(".")[-1]
    if file_suffix not in allow_suffix:
        return {"error": 1, "message": "图片格式不正确"}
    path, relative_path = upload_generation_dir(dir_name)
    file_name = str(uuid.uuid1()) + "." + file_suffix
    path_file = os.path.join(path, file_name)
    file_url = os.path.join(settings.MEDIA_URL + relative_path, file_name)
    open(path_file, 'wb').write(files.file.read())  # 保存图片
    return {"error": 0, "url": file_url}

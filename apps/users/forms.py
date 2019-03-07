__author__ = 'Hk4Fun'
__date__ = '2018/1/9 22:04'

from django import forms
from .models import User


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = User  # 选择要验证的表单model
        fields = ['image']  # 选择要验证的字段
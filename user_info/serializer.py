from django.contrib.auth.models import User
from rest_framework import serializers

class UserDescSerializer(serializers.ModelSerializer):#在文章中引用的嵌套序列化器，用于显示如姓名、性别等更具体的信息
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'last_login',
            'date_joined'
        ]
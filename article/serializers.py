from rest_framework import serializers
from .models import Article
from user_info.serializer import UserDescSerializer
from django_filters.rest_framework import DjangoFilterBackend

class ArticleSerializer(serializers.HyperlinkedModelSerializer): #自动提供了外键字段的超链接，并且默认不包含id字段
    author = UserDescSerializer(read_only=True)
    filterset_fields = ['author__username','title']
    class Meta:
        model = Article
        fields = '__all__'

"""
# 普通写法
# class ArticleListSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(allow_blank=True, max_length=100)
#     body = serializers.CharField(allow_blank=True)
#     created = serializers.DateTimeField()
#     updated = serializers.DateTimeField()

class ArticleListSerializer(serializers.ModelSerializer):
    author = UserDescSerializer(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="article:detail")  # view_name为路由名称，该行添加了超链接数据,自动完成动态地址映射

    class Meta:
        model = Article
        fields = [
            # 'id',  #有了路由就不再需要超链接
            'url',
            'title',
            'created',
            'author'
        ]
    # read_only_fields = ['author']
    # author字段设为只读,序列化器已设置只读，该行去掉


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
"""

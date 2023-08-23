from rest_framework import serializers
from .models import Article

# 普通写法
# class ArticleListSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(allow_blank=True, max_length=100)
#     body = serializers.CharField(allow_blank=True)
#     created = serializers.DateTimeField()
#     updated = serializers.DateTimeField()

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model= Article
        fields = [
            'id',
            'title',
            'created',
        ]
        read_only_fields = ['author'] #author字段设为只读

class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
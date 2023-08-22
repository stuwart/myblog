from django.shortcuts import render
from django.http import JsonResponse
from article.models import Article

from article.serializers import ArticleListSerializer

# Create your views here.

def article_list(request):
    articles = Article.objects.all()   #取出所有文章 QuerySet
    serializer = ArticleListSerializer(articles, many=True) # 创建序列化容器
    return JsonResponse(serializer.data, safe=False)  # 返回JSON格式数据


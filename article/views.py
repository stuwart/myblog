from django.shortcuts import render
from django.http import JsonResponse
from django.http import Http404

from article.models import Article

from article.serializers import ArticleListSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

@api_view(['GET', 'POST']) #允许视图接受  GET/POST
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()  # 取出所有文章 QuerySet
        serializer = ArticleListSerializer(articles, many=True)  # 创建序列化容器
        return JsonResponse(serializer.data, safe=False)  # 返回JSON格式数据
    elif request.method == 'POST':
        serializer = ArticleListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import render
from django.http import JsonResponse
from django.http import Http404

from article.models import Article

from article.serializers import ArticleListSerializer, ArticleDetailSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework.views import APIView


# Create your views here.

@api_view(['GET', 'POST'])  # 允许视图接受  GET/POST
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


class ArticleDetail(APIView):  # 文章详情
    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article, data=request.data)
        if serializer.is_valid():  # 若提交的数据合法，则反序列化后保存到数据库中
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = self.get_object(pk=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

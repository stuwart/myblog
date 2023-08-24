"""
from django.shortcuts import render
from django.http import JsonResponse
from django.http import Http404
# from article.serializers import ArticleListSerializer, ArticleDetailSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
"""

from article.models import Article
from article.permissions import IsAdminUserOrReadOnly
from rest_framework import viewsets, filters
from article.serializers import ArticleSerializer

from article.models import Category, Tag,Avatar
from article.serializers import CategorySerializer, TagSerializer, ArticleSerializer,ArticleDetailSerializer,AvatarSerializer


class ArticleViewSet(viewsets.ModelViewSet):  # 视图集将列表、详情逻辑都合在一起，并提供了增删改查的默认实现
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    # filterset_fields = ['author__username', 'title']  #用于精确搜索

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(author__username=username)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':  # 表示当前请求的动作为 ‘list’ 即获取列表
            return ArticleSerializer
        else:
            return ArticleDetailSerializer
    # def get_serializer_class(self): #视图集默认只提供一个序列化容器，覆写该方法可根据条件访问不同的序列化器
    #     if self.action == 'list':
    #         return SomeSerializer
    #     else:
    #         return Serializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class AvatarViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAdminUserOrReadOnly]

"""
# 最精简写法：
class ArticleList(generics.ListCreateAPIView):  # 通用视图
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer  # 序列化
    permission_classes = [IsAdminUserOrReadOnly]  # 接收一个列表，当前表示只有管理员有权限修改 ，另外可以用 IsAuthenticated AllowAny等

    def perform_create(self, serializer):  # 该函数在序列化数据保存前调用，可以在这里添加额外的数据
        serializer.save(author=self.request.user)  # serializer参数为Serializer序列化器实例，并已经携带验证后的数据


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAdminUserOrReadOnly]


"""

"""
Article_List 普通写法
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

"""

"""
使用Mixin的写法
class ArticleDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):  # 文章详情
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    #以下为普通写法
    # def get_object(self, pk):
    #     try:
    #         return Article.objects.get(pk=pk)
    #     except:
    #         raise Http404
    #
    # def get(self, request, pk):
    #     article = self.get_object(pk)
    #     serializer = ArticleDetailSerializer(article)
    #     return Response(serializer.data)
    #
    # def put(self, request, pk):
    #     article = self.get_object(pk)
    #     serializer = ArticleDetailSerializer(article, data=request.data)
    #     if serializer.is_valid():  # 若提交的数据合法，则反序列化后保存到数据库中
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, pk):
    #     article = self.get_object(pk=pk)
    #     article.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

"""

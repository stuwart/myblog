from rest_framework import serializers
from .models import Article, Category, Tag
from user_info.serializer import UserDescSerializer
from django_filters.rest_framework import DjangoFilterBackend


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.HyperlinkedModelSerializer):  # 分类的序列化器
    url = serializers.HyperlinkedIdentityField(view_name='category-detail')  # view_name为自动注册的路由名

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created']


class ArticleSerializer(serializers.HyperlinkedModelSerializer):  # HyperlinkedModelSerializer自动提供了外键字段的超链接，并且默认不包含id字段
    author = UserDescSerializer(read_only=True)
    # filterset_fields = ['author__username', 'title']
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, allow_null=True,
                                           required=False)  # 显式指定 category_id 字段，则此字段会自动链接到 category 外键，以便你更新外键关系。
    # 当一个关联字段希望使用字符串作为唯一标识而不是id时,就可以使用SlugRelatedField。
    tag = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False,
        slug_field='text'
    )

    # category_id字段验证器
    def validate_category_id(self, value):
        if not Category.objects.filter(
                id=value).exists() and value is not None:  # 如果没有找到id=value的那个标签并且value不是None，那么就报错：不存在
            raise serializers.ValidationError("Category with id {} not exists.".format(value))
        return value

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

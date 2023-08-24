from rest_framework import serializers
from .models import Article, Category, Tag
from user_info.serializer import UserDescSerializer
from django_filters.rest_framework import DjangoFilterBackend


class TagSerializer(serializers.HyperlinkedModelSerializer):
    def check_tag_obj_exist(self, validated_data):
        text = validated_data.get('text')
        if Tag.objects.filter(text=text).exists():
            raise serializers.ValidationError('Tag {} 已存在'.format(text))

    def create(self, validated_data):
        self.check_tag_obj_exist(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.check_tag_obj_exist(validated_data)
        return super().update(instance, validated_data)

    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.HyperlinkedModelSerializer):  # 分类的序列化器
    url = serializers.HyperlinkedIdentityField(view_name='category-detail')  # view_name为自动注册的路由名

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created']


class ArticleBaseSerializer(serializers.HyperlinkedModelSerializer):
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

    def validate_category_id(self, value):  # 验证category字段
        if not Category.objects.filter(
                id=value).exists() and value is not None:  # 如果没有找到id=value的那个标签并且value不是None，那么就报错：不存在
            raise serializers.ValidationError("Category with id {} not exists.".format(value))
        return value

    def to_internal_value(self, data):  # 若标签不存在就创建
        tags_data = data.get('tags')

        if isinstance(tags_data, list):  # 表示确认标签数据为列表，才会开始循环遍历
            for text in tags_data:
                if not Tag.objects.filter(text=text).exists():
                    Tag.objects.create(text=text)
        return super().to_internal_value(data)


class ArticleSerializer(ArticleBaseSerializer):  # HyperlinkedModelSerializer自动提供了外键字段的超链接，并且默认不包含id字段
    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {'body': {'write_only': True}}  # 让body字段不在列表显示


class ArticleDetailSerializer(ArticleBaseSerializer):
    body_html = serializers.SerializerMethodField()
    toc_html = serializers.SerializerMethodField()

    def get_body_html(self, obj):
        return obj.get_md()[0]

    def get_toc_html(self, obj):
        return obj.get_md()[1]

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

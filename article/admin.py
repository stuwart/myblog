from django.contrib import admin
from .models import Article, Category, Tag, Avatar

# Register your models here.

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Avatar)

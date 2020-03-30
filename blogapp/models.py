from django.core.paginator import PageNotAnInteger, Paginator
from django.db import models
import datetime

# Create your models here.
from django.shortcuts import render

from usetapp.models import BlogUser


class Banner(models.Model):
    """轮播图模型"""
    title = models.CharField('标题', max_length=50)
    cover = models.ImageField('轮播图', upload_to='static/')
    link_url = models.URLField('图片链接', max_length=100)
    idx = models.IntegerField('索引')
    is_active = models.BooleanField('是否是active', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = '轮播图'


class BlogCategory(models.Model):
    """博客分类模型"""
    name = models.CharField('分类名称', max_length=20, default='')

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = '博客分类'

    def __str__(self):
        return self.name


class Tags(models.Model):
    """标签类"""
    name = models.CharField('标签名称', max_length=20, default='')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def __str__(self):
        return self.name


class Post(models.Model):
    """博客模型"""
    user = models.ForeignKey(BlogUser, verbose_name='作者')
    category = models.ForeignKey(BlogCategory, verbose_name='博客分类', default=None)
    tags = models.ManyToManyField(Tags, verbose_name='标签')
    title = models.CharField('标题', max_length=50)
    content = models.TextField('内容')
    pub_date = models.DateTimeField('发布日期', default=datetime.now)
    cover = models.ImageField('博客封面', upload_to='static/images/post', default=None)
    views = models.IntegerField('浏览数', default=0)
    recommend = models.BooleanField('推荐博客', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = '博客'


class Comment(models.Model):
    """评论"""
    post = models.ForeignKey(Post, verbose_name='博客')
    user = models.ForeignKey(BlogUser, verbose_name='作者')
    pub_date = models.DateTimeField('发布时间')
    content = models.TextField('内容')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'


class FriendlyLink(models.Model):
    """友情链接"""
    title = models.CharField('标题', max_length=50)
    link = models.URLField('链接', max_length=50, default='')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = '友情链接'

class TagMessage(object):
    def __init__(self, tid, name, count):
        self.tid = tid
        self.name = name
        self.count = count

def blog_list(request):
    post_list = Post.objects.all()
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(post_list, per_page=1, request=request)

    post_list = p.page(page)

    tags = Tags.objects.all()
    tag_message_list = []
    for t in tags:
        count = len(t.post_set.all())
        tm = TagMessage(t.id, t.name, count)
        tag_message_list.append(tm)

    ctx = {
        'post_list': post_list,
        'tags': tag_message_list
    }
    return render(request, 'list.html', ctx)
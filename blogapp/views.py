from django.core.paginator import PageNotAnInteger, Paginator
from django.shortcuts import render
from .models import *


# Create your views here.
def index(request):
    banner_list = Banner.objects.all()
    recommend_list = Post.objects.filter(recommend=1)
    post_list = Post.objects.order_by('-pub_date').all()[:10]
    blogcategory_list = BlogCategory.objects.all()
    friendlylink_list = FriendlyLink.objects.all()
    ctx = {
        'banner_list': banner_list,
        'recommend_list': recommend_list,
        'post_list': post_list,
        'blogcategory_list': blogcategory_list,
    }
    return render(request, 'index.html', ctx)


def blog_list(request):
    post_list = Post.objects.all()
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(post_list, per_page=1, request=request)
    post_list = p.page(page)
    ctx = {
        'post_list': post_list,

    }
    return render(request, 'list.html', ctx)
def blog_list(request, cid=-1, tag_message_list=None):
    post_list = None
    if cid != -1:
       cat = BlogCategory.objects.get(id=cid)
       post_list = cat.post_set.all()
    else:
       post_list = Post.objects.all()



    ctx = {
        'post_list': post_list,
        'tags': tag_message_list
    }
    return render(request, 'list.html', ctx)

from django.views.generic.base import View
from django.db.models import Q


class SearchView(View):
    # def get(self, request):
    #     pass
    def post(self, request):
        kw = request.POST.get('keyword')
        post_list = Post.objects.filter(Q(title__icontains=kw) | Q(content__icontains=kw))

        ctx = {
            'post_list': post_list
        }
        return render(request, 'list.html', ctx)

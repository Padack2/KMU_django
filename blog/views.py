from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView
# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-pk'
    template_name = 'blog/post_list.html'

class PostDetail(DetailView):
    model = Post
    # template_name으로 지정하지 않으면 [모델명]_detail.html 자동인식
    # template_name = 'blog/post_detail.html'

# def index(request):
#     posts = Post.objects.all().order_by('-pk')
#
#     return render(
#         request,
#         'blog/post_list_back.html',
#         {
#             'posts': posts,
#         }
#     )

def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'blog/single_post_page.html',
        {
            'post': post,
        }
    )
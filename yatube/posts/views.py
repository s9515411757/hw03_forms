from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import Post, Group, User
from .forms import PostForm


def pagination(post_list, request):
    paginator = Paginator(post_list, settings.QUANTITY_POSTS)
    return paginator.get_page(request.GET.get('page'))


def index(request):
    post_list = Post.objects.select_related('author', 'group')
    page_obj = pagination(post_list, request)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.select_related('author', 'group').filter(group=group)
    page_obj = pagination(posts, request)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = User.objects.get(username=username)
    post_list = Post.objects.select_related('author', 'group').filter(
        author=author
    )
    page_obj = pagination(post_list, request)

    context = {
        'page_obj': page_obj,
        'post_count': post_list,
        'author': author,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post.objects.select_related(), pk=post_id)
    post_count = Post.objects.select_related('author', 'group').filter(
        author=post.author
    )

    context = {
        'post': post,
        'post_count': post_count,
        'author': post.author,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        forms = form.save(commit=False)
        forms.author = request.user
        forms.save()
        return redirect('posts:profile', request.user.username)
    else:
        context = {
            'form': form,
            'is_edit': False
        }
        return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related('author', 'group'), pk=post_id
    )
    if request.user != post.author:
        return redirect('posts:post_detail', post.id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail',  post.id)

    template = 'posts/create_post.html'
    form = PostForm(instance=post)

    context = {
        'form': form,
        'is_edit': True
    }
    return render(request, template, context)

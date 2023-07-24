from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import EmailPostForm

def post_list(request):
    posts = Post.published.all()
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})

def post_detail(request, year, month, day,post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish_year=year,
                             publish_month=month,
                             publish_day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})

def post_share(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form})
# Create your views here.

from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .forms import EmailPostForm, CommentForm
from django.views.decorators.http import require_POST


def post_share(request, post_id):
    # Извлечь пост по идентификатору
    post = get_object_or_404(Post,
                             id=post_id,
                             status = 'published')
    sent = False

    if request.method == 'POST':
        # Еслиформа передается в обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recomends you read" f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']} 's comments: {cd['comments']}"
            send_mail(subject,message, 'test.ecoupack.project@gmail.com', [cd ['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_list(request):
    object_list  = Post.published.all()
    paginator = Paginator(object_list, 3) #3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts,
                   'page': page})

def post_detail(request, year, month, day,post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active = True)
    form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments':comments,
                  'form': form})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id = post_id,
                             status = 'published')
    comment= None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post=post
        comment.save()
    return render(request, 'blog/post/comment.html',
                            {'post':post,
                             'form':form,
                             'comment': comment})
# Create your views here.

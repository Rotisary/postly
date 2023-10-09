from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.db.models import Q
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, PostComment
from users.decorators import allowed_users


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['?']
    paginate_by = 5


class LatestPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/latest_post.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5 



class PostDetailView(DetailView):
    model = Post 


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post 
    fields = ['title', 'content', 'image']


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post 
    fields = ['title', 'content', 'image']


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


def post_likes(request, pk):
            post = get_object_or_404(Post, id=pk)
            if post.likes.filter(id=request.user.id).first():
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
            
            likes_count = post.number_of_likes()
            data = {
                'likes_count': likes_count
            }
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class PostLikesAPI(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        post = get_object_or_404(Post, id=pk)
        updated = False
        liked = False

        if post.likes.filter(id=request.user.id).first():
            liked = False
            post.likes.remove(request.user)
        else:
            liked = True
            post.likes.add(request.user)
        updated = True
        counts = post.number_of_likes()
        data = {
            'updated': updated,
            'liked': liked,
            'likescount': counts
        }
            
        return Response(data)




class CommentCreateView(LoginRequiredMixin, CreateView):
    model = PostComment
    template_name = 'blog/create_comments.html'
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


class CommentListView(LoginRequiredMixin, ListView):
    model = PostComment
    context_object_name = 'comments'
    template_name = 'blog/comments.html'


    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        return PostComment.objects.filter(post=post).order_by('-posted_on')


    def get_context_data(self, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        context = super(CommentListView, self).get_context_data(**kwargs)
        context['post'] = Post.objects.filter(title=post).first()
        return context


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PostComment


    def get_success_url(self):
        objects = self.get_object()
        objects_id = objects.post.id
        return reverse('comments', kwargs={'pk': objects_id})

    def test_func(self): 
        comment = self.get_object()
        if comment.author == self.request.user:
            return True
        else:
            return False


def Search(request):
        search = request.GET.get('search')
        if search == '':
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            searched_content = Post.objects.filter(
                    Q(content__contains=search) | Q(title__contains=search)).order_by('-date_posted')
            searched_user = User.objects.filter(username__contains=search).order_by('-date_joined')
            context = {
                'search': search,
                'searched_content': searched_content,
                'searched_user': searched_user
            }
            return render(request, 'blog/search.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'about'})

@login_required
def trending(request):
    post_objects = Post.objects.all()
    posts = sorted(post_objects, key=lambda post: (-post.number_of_likes(), -post.number_of_comments()))
    return render(request, 'blog/trending.html', {'posts': posts})

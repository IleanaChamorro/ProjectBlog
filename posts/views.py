from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, PostView, Like, Comment, DisLike
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .form import PostForm

class PostListView(ListView):
    model = Post

class PostDetailView(DetailView):
    model = Post

class PostCreateView(CreateView):
    form_class = PostForm
    model = Post
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'create'
        })
        return context
    
    

class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context
    
class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

def like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like_qs = Like.objects.filter(user=request.user, post=post)

    #If like exits
    if like_qs.exists():
        like_qs[0].delete()
        return redirect('detail', slug=slug)

    #If like don't exits
    Like.objects.create(user=request.user, post=post)
    return redirect('detail',slug=slug)
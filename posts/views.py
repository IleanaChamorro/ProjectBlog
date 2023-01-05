from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, PostView, Like, Comment, DisLike
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .form import PostForm, CommentForm

class PostListView(ListView):
    model = Post

class PostDetailView(DetailView):
    model = Post

    def post(self, *args, **kwargs):
        form = CommentForm(self.request.POST)
    
    #If the form is valid, an instance of it is obtained so that the user can leave a comment
        if form.is_valid():
            post = self.get_object()
            comment = form.instance
            comment.user = self.request.user
            comment.post = post
            comment.save()
            #After the user leaves their comment,he is redirected to the home
            return redirect("detail", slug=post.slug)

        return redirect("detail", slug=self.get_object().slug)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form': CommentForm()
        })
        return context
    
    #View Counter
    def get_object(self, **kwargs):
        object = super().get_object(**kwargs)
        #The view is only counted if the user is authenticated
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(user=self.request.user, post=object)
        return object


#Create a Post
class PostCreateView(CreateView):
    form_class = PostForm
    model = Post
    #After creating the post, the user is redirected to home
    success_url = '/'


    #Get data to create post 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'create'
        })
        return context
    
#Update Post View
class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    #After updating the post, the user is redirected to home
    success_url = '/'

    #Get data to update the post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context
    
#Delete Post
class PostDeleteView(DeleteView):
    model = Post
    #After deleting the post, the user is redirected to home
    success_url = '/'

def like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like_qs = Like.objects.filter(user=request.user, post=post)

    #In case the like exists, the user can remove his like
    if like_qs.exists():
        like_qs[0].delete()
        return redirect('detail', slug=slug)

    #In case the user has not given a like, he can do it
    Like.objects.create(user=request.user, post=post)
    return redirect('detail',slug=slug)

def dislike(request, slug):
    post = get_object_or_404(Post, slug=slug)
    dislike_qs = DisLike.objects.filter(user=request.user, post=post)

    #In case the dislike exists, the user can remove his dislike 
    if dislike_qs.exists():
        dislike_qs[0].delete()
        return redirect('detail', slug=slug)

    #In case the user has not given a like, he can do it
    DisLike.objects.create(user=request.user, post=post)
    return redirect('detail',slug=slug)
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, PostView, Like, Comment, DisLike
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .form import PostForm, CommentForm

class PostListView(ListView):
    model = Post

class PostDetailView(DetailView):
    model = Post

    #Comentarios de usuarios
    def post(self, *args, **kwargs):
        form = CommentForm(self.request.POST)
    
    #Si el formulario es valido, se obtiene una instancia de este para que el usuario pueda dejar un comentario
        if form.is_valid():
            post = self.get_object()
            comment = form.instance
            comment.user = self.request.user
            comment.post = post
            #Guardar comentario
            comment.save()
            #Luego de realizar el comentario, se redirige al home
            return redirect("detail", slug=post.slug)

        #En caso de que no sea valido el post
        return redirect("detail", slug=self.get_object().slug)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form': CommentForm()
        })
        return context
    
    #Contar vistas de usuario
    def get_object(self, **kwargs):
        object = super().get_object(**kwargs)
        #Si el usuario esta autenticado se cuenta la vista 
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(user=self.request.user, post=object)
        return object


#Crear Post 
class PostCreateView(CreateView):
    form_class = PostForm
    model = Post
    #Una vez creado, redirigir al home
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'create'
        })
        return context
    
#Actualizar Post
class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    #Una vez  actualizado, redirigir al home
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context
    
#Borrar Post
class PostDeleteView(DeleteView):
    model = Post
    #Una vez borrado el post, redirigir al home
    success_url = '/'

def like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like_qs = Like.objects.filter(user=request.user, post=post)

    #En caso de que el like exista el usuario puede sacar su like 
    if like_qs.exists():
        like_qs[0].delete()
        return redirect('detail', slug=slug)

    #En caso de que el usuario no haya dado like, puede hacerlo 
    Like.objects.create(user=request.user, post=post)
    return redirect('detail',slug=slug)
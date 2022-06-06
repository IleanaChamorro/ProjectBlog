from django import forms 
from .models import Post, Comment

class PostForm(forms.ModelForm):    
    class Meta:
        model = Post
        fields = ('__all__')


#Comentarios
class ComentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
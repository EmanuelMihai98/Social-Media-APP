from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "content_description"]
        widgets = {
            "content": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/*,video/*"
            }),
            "content_description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Tell something about your post",
                "rows": 3
            })
        }
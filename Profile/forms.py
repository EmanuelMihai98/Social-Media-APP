from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["display_name", "bio", "profile_pic"]
        widgets = {
            "display_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your display name"
            }),
            "bio": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Tell something about you",
                "rows": 4
            }),
            "profile_pic": forms.FileInput(attrs={
                "class": "form-control"
            })
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "placeholder": "Choose your username",
            "class": "w-full px-4 py-4 border-2 border-gray-200 roun"
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'your.email@example.com',
            'class': 'w-full px-4 py-4 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all duration-300 outline-none text-lg'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Create a password',
            'class': 'w-full px-4 py-4 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all duration-300 outline-none text-lg'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm your password',
            'class': 'w-full px-4 py-4 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all duration-300 outline-none text-lg'
        })

    def email_check(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")
        return email
    

class UserLoginForm(AuthenticationForm):
        username = forms.CharField(widget=forms.TextInput(attrs={
            "placeholder": "Username",
            'class': 'w-full px-4 py-4 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all duration-300 outline-none text-lg'
        }))
        password = forms.CharField(widget=forms.PasswordInput(attrs={
            "placeholder": "Username",
            'class': 'w-full px-4 py-4 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all duration-300 outline-none text-lg'
        }))


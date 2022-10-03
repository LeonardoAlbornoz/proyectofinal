from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User  
from .models import Chat

class AgregarBlog(forms.Form):
    titulo = forms.CharField(		label='Título     ', max_length=20)
    texto_corto = forms.CharField(	label="Texto Corto", max_length=40)
    texto_largo = forms.CharField(	label="Texto Largo", widget=forms.Textarea)
    imagen = forms.ImageField(		label="Imagen     ")

class UserChangeForm(UserChangeForm):
    username = forms.CharField(required=False, disabled=True)
    email = forms.EmailField(required=False)
    last_name = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    date_joined = forms.DateField(required=False, disabled=True)
    last_login = forms.DateField(required=False, disabled=True)
    password = None
    class Meta: 
        model = User
        fields = ('username','first_name', 'last_name', 'email')

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class chatform(forms.ModelForm):
    mensaje = forms.CharField(label='Dejar Mensaje     ', max_length=150,widget=forms.Textarea(attrs={'style':'resize: none;background: transparent;color:cornsilk; width: -webkit-fill-available', 'rows':'3','autofocus':''}))
    class Meta:
        model=Chat
        fields = ("mensaje",)
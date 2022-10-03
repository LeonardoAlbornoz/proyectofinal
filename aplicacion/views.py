from django.shortcuts import render, redirect
from .forms import AgregarBlog, UserChangeForm, UserCreationForm, chatform
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from aplicacion.models import Blog, Chat
import os
# Create your views here.

def index(request):
    dicctionary = {} 
    bobjects = Blog.objects.all()       # -------- Agarra todos los objetos de Blog y los guarda como queryset en la variable b(log)objects
    dicctionary["bobjects"] = bobjects  # -- agrega bobjects en el diccionario del contexto 
    if request.method == 'POST':
            form = AgregarBlog(request.POST, request.FILES)
            if form.is_valid():
                titulo = form.cleaned_data.get("titulo")
                texto_corto = form.cleaned_data.get("texto_corto")
                texto_largo = form.cleaned_data.get("texto_largo")
                imagen = form.cleaned_data.get("imagen")
                obj = Blog.objects.create(
                    titulo = titulo,
                    imagen = imagen,
                    texto_corto = texto_corto,
                    texto_largo = texto_largo,
                    autor = request.user.username)
                obj.save()
                dicctionary['respuesta_add'] = "Agregado correctamente"
    form = AgregarBlog()
    dicctionary['form'] = form
    return render(request, "index_hijo.html", dicctionary)

def about(request):

    return render(request, "about.html", {})

def single_view(request, id):
    dicctionary = {}
    bobjects = Blog.objects.filter(id=id)
    dicctionary["svobj"] = bobjects

    return render(request, "singleview.html", dicctionary)

def perfil(request, perfil):
    dicctionary = {}
    usuario = request.user
    data = User.objects.get(username=perfil)
    form = UserChangeForm(initial={
            'first_name': data.first_name,
            'email': data.email,
            'last_login': data.last_login,
            'last_name': data.last_name,
            'username': data.username,
            'date_joined': data.date_joined,
        })
        
    dicctionary['form'] = form
    chatobj = Chat.objects.filter(usuario_to=perfil)
    dicctionary["chatobj"] = chatobj    
    if request.user.username == perfil:
        dicctionary['iguales'] = "si"
        passw = PasswordChangeForm(user=request.user)
        dicctionary['passw'] = passw
        if request.method == 'POST':
            if request.POST.get('editstuff'):
                form = UserChangeForm(request.POST)
                if form.is_valid():
                    data = form.cleaned_data
                    print(data)
                    print(data['email'])
                    usuario.email = data['email']
                    usuario.first_name = data['first_name']
                    usuario.last_name = data['last_name']
                    usuario.save()
                    dicctionary['mensaje'] = "Cambiado correctamente"
                else: 
                    print("form not valid")
                    dicctionary['errores'] = form.errors
                    print(form.errors)
            elif request.POST.get('cleanchat'):
                chatobj = Chat.objects.filter(usuario_to=perfil).delete()
                print(chatobj)
            else:
                passwform = PasswordChangeForm(user=request.user, data=request.POST)
                if passwform.is_valid():
                    print("passwrform")
                    print(passwform)

                    passwform.save()
                    update_session_auth_hash(request, passwform.user)
                    dicctionary['mensaje'] = "Password cambiado"
                else:
                    print("passwd no valid")
                    dicctionary['erroresp'] = passwform.error_messages
                    print(passwform.error_messages)
                    print(passwform.errors)
    else: #EL PERFIL QUE ENTRASTE NO ES EL MISMO QUE EL USUARIO LOGUEADO
            if request.method == 'POST':
                chatf = chatform(request.POST)
                if chatf.is_valid():
                    mensaje = chatf.cleaned_data.get("mensaje")
                    obj = Chat.objects.create(
                    mensaje = mensaje,
                    usuario_to = perfil,
                    usuario_from = usuario.username)
                    obj.save()
                else:
                    print("chatf no es valido")
                    print(chatf.errors)
            chatf = chatform()
            dicctionary['chatf'] = chatf

    
    return render(request, "perfil.html", dicctionary)

def create(request):
    dicctionary = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', False)
            password1 = request.POST.get('password1', False)
            email = request.POST.get('email', False)
            createacc =    User.objects.create_user(username, email, password1)
            createacc.save()
            dicctionary['mensaje'] = "Cuenta creada satisfactoriamente!"
            return render(request, "create.html", dicctionary)
        else:
            print("invalid")
            dicctionary['errores'] = form.errors
            print(form.errors)
    form = UserCreationForm()
    dicctionary['form'] = form
    return render(request, "create.html", dicctionary)


def edit_blog(request, id):
    dicctionary = {}
    if request.method == 'POST':
            form = AgregarBlog(request.POST, request.FILES)
            if form.is_valid():
                titulo = form.cleaned_data.get("titulo")
                texto_corto = form.cleaned_data.get("texto_corto")
                texto_largo = form.cleaned_data.get("texto_largo")
                try:
                    post = Blog.objects.get(id=id)
                    try:
                        os.remove(post.imagen.path)
                        print('Old post image deleted...! path = '+str(post.imagen.path))
                    except Exception as e:
                        print('No image for delete '+str(e))
            
                    post.imagen = request.FILES['imagen'] #Worked..
                
                    post.save()
                except Exception as e:
                    print(e)
            Blog.objects.filter(id=id).update(
                autor = request.user.username,
                titulo = titulo,
                texto_corto = texto_corto,
                texto_largo = texto_largo)
            dicctionary['respuesta_add'] = "Editado correctamente"
    else:
        data = Blog.objects.get(id=id)
        form = AgregarBlog(initial={
            'titulo' : data.titulo,
            'texto_corto' : data.texto_corto,
            'texto_largo' : data.texto_largo,
        })
        dicctionary['form'] = form
    return render(request, "edit_blog.html", dicctionary)

def delete_blog(request, id):
    #primero intenta borrar la imagen del sistema y luego borra la entrada de la DB
    try:
                post = Blog.objects.get(id=id)
                try:
                    os.remove(post.imagen.path)
                    print('Old post image deleted...! path = '+str(post.imagen.path))
                except Exception as e:
                    print('No image for delete '+str(e))
            
    except Exception as e:
                print(e)
    Blog.objects.filter(id=id).delete()
    return redirect(index)   
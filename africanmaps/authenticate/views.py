from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User

# Mobile 

def login_mobile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Vous avez été connecté avec succès')
            return redirect('map_mobile')
        else:
            messages.warning(request, "Le nom d'utilisateur ou le mot de passe est incorrect !!")
            return redirect('login')
    return render(request, 'authenticate/login_mobile.html')


def logout_mobile(request):
    logout(request)
    messages.success(request, "Déconnexion réussie")
    return redirect('login_mobile')


# Web

def home(request):
    return render(request, 'authenticate/home.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in successfully')
            return redirect('dashboard')
        else:
            messages.warning(request, "Username or Password is incorrect !!")
            return redirect('login')
    return render(request, 'authenticate/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "Déconnexion réussie")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        user_type = request.POST['user_type']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.warning(request, "Username already exists")
            elif User.objects.filter(email=email).exists():
                messages.warning(request, "Email already exists")
            else:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password1
                )
                # تعيين نوع المستخدم
                if user_type == 'admin':
                    user.is_staff = True  # جعله موظفًا
                    user.is_superuser = True  # جعله أدمن
                user.save()  # حفظ المستخدم
                messages.success(request, "Account created successfully")
                login(request, user)
                return redirect('home')
        else:
            messages.warning(request, "Passwords do not match")
    return render(request, 'authenticate/register.html')

def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        messages.success(request, "Profile Updated Successfully")
        return redirect('home')
    return render(request, 'authenticate/edit_profile.html', {'user': request.user})

def change_password(request):
    if request.method == 'POST':
        user = request.user
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        if user.check_password(old_password):
            if new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password Changed Successfully")
                return redirect('home')
            else:
                messages.warning(request, "New passwords do not match")
        else:
            messages.warning(request, "Old password is incorrect")
    return render(request, 'authenticate/change_password.html')

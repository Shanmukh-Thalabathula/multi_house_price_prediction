from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from . models import RecentActivity
# Create your views here.

# user registration
def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login')

    return render(request, 'users/register.html')


# user login
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect if already logged in

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to prediction page after login
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'users/login.html')

@login_required
def recent_activities(request):
    activities = RecentActivity.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'users/recent_activities.html', {'activities': activities})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def delete_activity(request, activity_id):
    activity = get_object_or_404(RecentActivity, id=activity_id, user=request.user)
    activity.delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})

    return redirect('recent_activities')  # Adjust to your URL name


@login_required
def delete_activity(request, activity_id):
    activity = get_object_or_404(RecentActivity, id=activity_id, user=request.user)
    activity.delete()
    return redirect('recent_activities')  # Redirect back to recent activities page

def project_description(request):
    return render(request, 'users/description.html')
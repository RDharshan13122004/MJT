from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib.auth.hashers import make_password, check_password
from .forms import UserLoginForm

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']
            #print(user_id, password)
            try:
                user = UserProfile.objects.get(user_id=user_id)
            except UserProfile.DoesNotExist:
                return render(request, 'login.html', {
                    'form': form,
                    'error': 'Invalid User ID'
                })

            # Check password
            if check_password(password, user.password) == False:
                return render(request, 'login.html', {
                    'form': form,
                    'error': 'Incorrect Password'
                })
            request.session['user_id'] = user.user_id
            request.session['user_name'] = user.user_name
            request.session['role'] = user.role
            return redirect('tracking:dashboard')

        # Form invalid
        return render(request, 'login.html', {'form': form})

    # GET request → show login page
    form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        password = request.POST.get('password')

        if user_id and user_name and email and role and password:
            hashed_password = make_password(password)
            UserProfile.objects.create(
                user_id=user_id,
                user_name=user_name,
                email=email,
                phone=phone,
                role=role,
                password=hashed_password
            )
            return redirect('users:user_login')
        else:
            return render(request, 'signup.html', {'error': 'Please fill all required fields.'})
    return render(request, 'signup.html')
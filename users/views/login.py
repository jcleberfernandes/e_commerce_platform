from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, 'users/login.html', {'error': 'Credenciais inválidas.'})

        login(request, user)
        return redirect('/')

    return render(request, 'users/login.html')
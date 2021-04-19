from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from contacts.models import Contact
from django.urls import reverse


# Create your views here.
def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST.get('first_name', False)
        last_name = request.POST.get('last_name', False)
        username = request.POST.get('username', False)
        email = request.POST.get('email', False)
        password = request.POST.get('password', False)
        password2 = request.POST.get('password2', False)
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        # username = request.POST['username']
        # email = request.POST['email']
        # password = request.POST['password']
        # password2 = request.POST['password2']
        # check if password match
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error (request, 'That username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error (request, 'That Email has taken by someone else')
                    return redirect('register')
                else:
                    # Registration  now is possible
                    user = User.objects.create_user(username=username, password=password, email=email, first_name = first_name, last_name=last_name)
                    # Login after Registration
                    # auth.login(request, user)
                    # messages.success(request, ' Successfully you are logged in')
                    # return redirect('register')
                    user.save()
                    messages.success(request, ' Successfully registered')
                    return redirect('login')

        else:
            messages.error(request, 'password do not match')
            return redirect ('register')

    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, ' Welcome '+ user.first_name + ' you are Successfully logged in')
            return redirect('dashboard')
        else:
            messages.error (request, 'Invalid Account')
            return redirect('login')
        return 
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are logged out')
        return redirect(reverse('index'))

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)

 
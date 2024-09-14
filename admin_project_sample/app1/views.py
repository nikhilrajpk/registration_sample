from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User



# Create your views here.
@never_cache
def loginPage(request):
    result = ""
    print('login')
    if request.user.is_authenticated:
        return redirect(home)
    if request.method == 'POST':
        username = request.POST.get('username')        
        password = request.POST.get('password')
        print(username)
        user = authenticate(request, username = username, password = password)
        print(user)
        print('login in')
        if user is not None:
            print('login if')
            login(request,user)
            if user.is_staff:
                return redirect(adminPage)
            else:
                print('login else')
                return redirect(home)
        else:
            print('out else')
            result = "username or password is incorrect!"
            return render(request,'login.html',{'result':result})
    else:
        return render(request,'login.html')

@never_cache
def signupPage(request):
    print('signup')
    if request.user.is_authenticated:
        return redirect(home)
    if request.method == 'POST':
        print('inside')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        if password == c_password:
            user_obj = User.objects.create_user(username = username, email = email, password = password)
            user_obj.save()
            print('in')
            return redirect(loginPage)
        else:
            result = 'password mismatch'
            return render(request, 'signup.html',{'result':result})
    return render(request, 'signup.html')
@never_cache
def home(request):
    if request.user.is_staff:
        return redirect(adminPage)
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'home.html',{'user':user})
    return redirect(loginPage)

@never_cache
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(loginPage)

@never_cache
@login_required
def adminPage(request):
    if request.user.is_staff:
        query = request.GET.get('query')
        print(query,'ha')
        if query:
            print(query)
            user_obj = User.objects.filter(is_staff = False).filter(username__icontains = query) | User.objects.filter(is_staff = False).filter(email__icontains = query)
        else:
            user_obj = User.objects.filter(is_staff = False)
        context = {'user_obj' : user_obj, 'query' : query}
        return render(request, 'admin.html', context)
    else:
        return redirect(loginPage)

@never_cache
def create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user_obj = User(username = username, email = email, password = password)
        user_obj.save()
        return redirect(adminPage)
    return render(request, 'admin.html')

@never_cache
def update(request,id):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        user_obj = User(
            id = id,
            username = username,
            email = email,
        )
        user_obj.save()
        
        # return redirect(adminPage)
    return render(request, 'admin.html')

@never_cache
def delete(request,id):
    if request.method == 'POST':
        user_obj = User.objects.filter(id = id)
        user_obj.delete()
        return redirect(adminPage)
    else:
        return render(request,'admin.html')
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm,AddCustomerForm
from .models import record

def home(request):
    records = record.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Authenticate 
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You Logged in successfully")
            return redirect('home')
        else:
            messages.success(request,"There was an error loging in please try again...")
            return redirect('home')
    else:    
        return render(request,'home.html',{'records':records})


def logout_user(request):
    logout(request)
    messages.success(request,"You've been logged out")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Auth user and login to site
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('home')
    else:
        form = SignUpForm()   
        return render(request,'register.html',{'form':form})
    return render(request,'register.html',{'form':form})

def customer_record(request,pk):
    if request.user.is_authenticated:
        customer_record = record.objects.get(id=pk )
        return render(request,'record.html',{'customer_record':customer_record})
    else:
        messages.success(request,"You must login in :)")
        return redirect('home')    
def delete_customer(request,pk):
    if request.user.is_authenticated:
        delete_it = record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,'Customer deleted succesfully')
        return redirect('home')
    else:
        messages.success(request,"You must login in :)")
        return redirect('home')


def add_customer(request):
    form = AddCustomerForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
        return render(request, 'add_customer.html', {'form':form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')

def update_customer(request,pk):
    if request.user.is_authenticated:
        current_record = record.objects.get(id=pk)
        form = AddCustomerForm(request.POST or None,instance=current_record)
        if form.is_valid():
            form.save() 
            messages.success(request, "Customer info updated")
            return redirect('home')
        return render(request, 'update_customer.html', {'form':form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')
        
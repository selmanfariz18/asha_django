from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from ashaease.models import ProfileDetail



# Create your views here.


def base(request):
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email=request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            else:
                # create user and profile objects
                user = User.objects.create_user(
                    username=username, password=password,email=email)
                user.save()

                messages.success(request, 'Account created successfully.')
                return render(request, 'register.html')
        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect('register')
    return render(request, 'register.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password'] 

        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request=request, user=user)          
            if user.is_superuser:
                messages.error(request, "Password/email incorrect")
                return render(request, 'register.html')
            else:
                try:
                    user_detail = ProfileDetail.objects.get(user=request.user)
                except ProfileDetail.DoesNotExist:
                    user_detail = ProfileDetail(user=request.user)

                if(user_detail.is_updated == False):
                    return HttpResponseRedirect(reverse("edit_profile"))
                else:
                    return HttpResponseRedirect(reverse("home"))
        else:
            messages.error(request, "Password/email incorrect")
            return render(request, 'register.html')   
        
def edit_profile(request):

    if request.method == 'POST':
        name = request.POST['name']
        district=request.POST['district']
        asha_id = request.POST['asha_id']
        health_center = request.POST['health_center']
        mobile_no = request.POST['mobile_no']        
        issue_date = request.POST['issue_date']
        expiry_date = request.POST['expiry_date']
        dob = request.POST['dob']
        blood_group = request.POST['blood_group']
        aadhar_no = request.POST['aadhar_no']
        address = request.POST['address']
        office_address = request.POST['office_address']

        if request.user.is_authenticated:
            request.user.first_name = name
            request.user.save()

        try:
            profile = ProfileDetail.objects.get(user=request.user)
        except ProfileDetail.DoesNotExist:
            profile = ProfileDetail(user=request.user)
        profile.user = request.user
        profile.district = district
        profile.asha_id = asha_id
        profile.health_center = health_center
        profile.mobile_no = mobile_no
        profile.issue_date = issue_date
        profile.expiry_date = expiry_date
        profile.dob = dob
        profile.blood_grp = blood_group
        profile.aadhar_no = aadhar_no
        profile.address = address
        profile.office_address = office_address
        profile.is_updated = True
        profile.save()

        return HttpResponseRedirect(reverse("home"))
        # print(name, district, asha_id, health_center, mobile_no,issue_date, expiry_date,
        #       dob, blood_group, aadhar_no, address, office_address)

    return render(request, 'edit_profile.html')

def logout_user(request):
    logout(request)
    messages.success(request, "Logout Successfull!")
    return render(request, 'base.html')

def home(request):
    return render(request, 'home.html')
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from .forms import EventForm
from django.http import JsonResponse
from .models import Report,Heading, Questions
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.dateparse import parse_date


from datetime import datetime
import datetime

from ashaease.models import ProfileDetail, Event



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

def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        if not request.user.is_authenticated:
            return HttpResponse('Not logged in correctly!', status=401)

        if not check_password(old_password, request.user.password):
            messages.error(request, 'Your old password was entered incorrectly!')
            return render(request, 'change_password.html')

        if new_password != confirm_new_password:
            messages.error(request, 'The two password fields didnt match.')
            return render(request, 'change_password.html')

        # If all is good, set new password and save the user model
        request.user.password = make_password(new_password)
        request.user.save()

        # Updating session with the new password hash
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Your password has been changed successfully!')
        return redirect('home')  

    return render(request, 'change_password.html')

@login_required
def calendar(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('calendar')
    else:
        form = EventForm()

    today = datetime.date.today()
    events = Event.objects.filter(user=request.user, event_date__year=today.year, event_date__month=today.month)
    return render(request, 'calendar.html', {'form': form, 'events': events})

@login_required
def get_events(request, year, month):
    events = list(Event.objects.filter(
        user=request.user,
        event_date__year=year,
        event_date__month=month
    ).values())
    return JsonResponse(events, safe=False)

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('calendar')
    else:
        form = EventForm(instance=event)
    return render(request, 'edit_event.html', {'form': form})

from datetime import date

def get_events_by_day(request, year, month, day):
    event_date = date(year, month, day)
    events = Event.objects.filter(event_date=event_date)
    events_data = [{"title": event.title, "date": event.event_date, "start_time": event.start_time, "end_time": event.end_time} for event in events]
    return JsonResponse(events_data, safe=False)

import vonage

def notification(request):
    if request.method == 'POST':
        # mobile = request.POST['mobile']
        message=request.POST['message']
        client = vonage.Client(key="387d2351", secret="PeVmQ28XjdEwAbzQ")
        sms = vonage.Sms(client)

        responseData = sms.send_message(
            {
                "from": "Vonage APIs",
                "to": "919074516544",
                "text": str(message),
            }
        )

        if responseData["messages"][0]["status"] == "0":
            print("Message sent successfully.")
        else:
            print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
        messages.success(request, 'Notification send successfully!')
        return redirect('home')

    return render(request, 'notification.html')


def report(request):

    if request.method == "POST":
        # Get data from form
        # report_name = request.POST.get('report_name')
        date = request.POST.get('date')
        request.session['report_date'] = {
            'date': date,
            # 'heading_id': heading.id
        }

        return redirect('report')

    try:
        date = request.session.pop('report_date')
        if date:
            # Extract data
            date = date.get('date')
        reports = Report.objects.filter(created_by=request.user, date= date)
    except:
        reports = Report.objects.filter(created_by=request.user)

    context = {
        'reports' : reports,
    }    

    return render(request, 'report.html', context)

def report_edit(request):

    if request.method == "POST":
        # Get data from form
        report_name = request.POST.get('report_name')
        report_date = request.POST.get('report_date')
        heading = request.POST.get('heading')
        question = request.POST.get('question')
        count = request.POST.get('count')

        # Parse the date from string to date object
        report_date = parse_date(report_date)

        # Assuming the user is logged in and is available as request.user
        user = request.user

        # Retrieve the existing report or create a new one if it doesn't exist
        report, report_created = Report.objects.get_or_create(
            name=report_name, 
            date=report_date, 
            defaults={'created_by': user}
        )

        # Retrieve or create the heading under the report
        heading, heading_created = Heading.objects.get_or_create(
            report=report,
            heading=heading
        )

        # Create a new question under the heading
        question = Questions.objects.create(
            heading=heading,
            question_text=question,
            count=count
        )

        report = Report.objects.get(created_by=request.user, id=report.id) 
        heading = Heading.objects.filter(report=report)
        questions = Questions.objects.all()



        # context = {
        #     'reports' : report,
        #     'heading' : heading,
        #     'questions' : questions
        # }
        # # print()
        # return render(request, 'edit_report_maintain.html', context)
        # Process form data and save to session
        request.session['report_data'] = {
            'report_id': report.id,
            # 'heading_id': heading.id
        }

        # Redirect to the maintain view
        return redirect('report_edit_maintain')

    return render(request, 'edit_report.html')


def report_edit_maintain(request):
    if request.method == "POST":
        # Get data from form
        report_name = request.POST.get('report_name')
        report_date = request.POST.get('report_date')
        heading = request.POST.get('heading')
        question = request.POST.get('question')
        count = request.POST.get('count')

        # Parse the date from string to date object
        report_date = parse_date(report_date)

        # Assuming the user is logged in and is available as request.user
        user = request.user

        # Retrieve the existing report or create a new one if it doesn't exist
        report, report_created = Report.objects.get_or_create(
            name=report_name, 
            date=report_date, 
            defaults={'created_by': user}
        )

        # Retrieve or create the heading under the report
        heading, heading_created = Heading.objects.get_or_create(
            report=report,
            heading=heading
        )

        # Create a new question under the heading
        question = Questions.objects.create(
            heading=heading,
            question_text=question,
            count=count
        )

    
        reports = Report.objects.get(created_by=request.user, id=report.id) 
        heading = Heading.objects.filter(report=reports)
        questions = Questions.objects.all()


        context = {
            'reports' : reports,
            'heading' : heading,
            'questions' : questions
        }
        return render(request, 'edit_report_maintain.html', context)

    data = request.session.pop('report_data', None)
    if data:
            # Extract data
        report_id = data.get('report_id')
        # heading_id = data.get('heading_id')

    
    reports = Report.objects.get(created_by=request.user, id=report_id)
    heading = Heading.objects.filter(report=reports)
    questions = Questions.objects.all()

    request.session['report_data'] = {
        'report_id': report_id,
            # 'heading_id': heading.id
    }

    context ={
        'reports' : reports,
        'heading' : heading,
        'questions' : questions,
    }

    return render(request, 'edit_report_maintain.html', context)

def report_view(request):
    if request.method == "POST":
        # Get data from form
        id = request.POST.get('id')
        reports = Report.objects.get(created_by=request.user, id=id)
        heading = Heading.objects.filter(report=reports)
        questions = Questions.objects.all()

        request.session['report_data'] = {
            'report_id': id,
                # 'heading_id': heading.id
        }

        context ={
            'reports' : reports,
            'heading' : heading,
            'questions' : questions,
        }

        return render(request, 'edit_report_maintain.html', context)
    

def report_delete(request):
    if request.method == "POST":
        # Get data from form
        id = request.POST.get('id')

        report = get_object_or_404(Report, id=id)
        report.delete()

        return redirect('report')
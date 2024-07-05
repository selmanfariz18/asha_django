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
from .models import Report,Heading, Questions, House, Members, Children, Pregnant, Patient
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

    try:
        profile = ProfileDetail.objects.get(user=request.user)
    except ProfileDetail.DoesNotExist:
        profile = ProfileDetail(user=request.user) 

    

    return render(request, 'edit_profile.html', {'profile' : profile, 'user': request.user})

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

    # today = datetime.date.today()
    # events = Event.objects.filter(user=request.user, event_date__year=today.year, event_date__month=today.month)
    events = Event.objects.filter(user=request.user,).order_by('-event_date')
    return render(request, 'calendar.html', {'form': form, 'events': events})

def delete_event(request):
    if request.method == 'POST':
        id = request.POST['id']
        event = get_object_or_404(Event, id=id)
        event.delete()
        return HttpResponseRedirect(reverse("calendar"))


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
    
def house_hold(request):
    if request.method == "POST":
        house_no = request.POST.get('house_no')
        house_address = request.POST.get('house_address')
        no_of_members = request.POST.get('no_of_members')
        pregnant_onboard = request.POST.get('pregnant_onboard')
        if pregnant_onboard == 'True':
            pregnant_onboard = True
            pregnant_cound = request.POST.get('pregnant_cound')
        else:
            pregnant_onboard = False
        patients_onboard = request.POST.get('patients_onboard')
        if patients_onboard == 'True':
            patients_onboard = True
            patients_cound = request.POST.get('patients_cound')
        else:
            patients_onboard = False
        child_onboard = request.POST.get('child_onboard')
        if child_onboard == 'True':
            child_onboard = True
            child_cound = request.POST.get('child_cound')
        else:
            child_onboard = False

        # print(pregnant_onboard, pregnant_cound, patients_onboard, child_onboard)

        house = House(user=request.user)

        house.house_no = house_no
        house.house_address = house_address
        house.no_of_members = no_of_members
        house.pregnant_onboard = pregnant_onboard
        if pregnant_onboard == True:
            house.pregnant_cound = pregnant_cound
        else:
            house.pregnant_cound = 0
        house.patients_onboard = patients_onboard
        if patients_onboard == True:
            house.patients_cound = patients_cound
        else:
            house.patients_cound = 0
        house.child_onboard = child_onboard
        if child_onboard == True:
            house.child_cound = child_cound
        else:
            house.child_cound = 0
        house.save()

        return redirect('house_hold')

    house = House.objects.filter(user=request.user)

    context = {
        'house' : house
    }

    return render(request, 'household.html', context)

def search_house_hold(request):
    if request.method == "POST":
        house_no = request.POST.get('house_no')       

        house = House.objects.filter(user=request.user, house_no=house_no )

        context = {
            'house' : house
        }

        return render(request, 'search_household.html', context)

def add_member_request(request):
    if request.method == "POST":
        id = request.POST.get('id')
        house = House.objects.get(id=id)
        return render(request, 'add_members.html', {'id':id, 'house': house})

def add_member(request):
    if request.method == "POST":
        id = request.POST.get('id')
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        qualification = request.POST.get('qualification')
        occupation = request.POST.get('occupation')
        habit = request.POST.get('habit')
        if habit == 'True':
            habit = True
            habittype = request.POST.get('habittype')
        else:
            habit = False

        # print(id, dob, age, habit)

        house = House.objects.get(id=id)

        member = Members(house=house)
        member.name = name
        member.gender = gender
        member.dob = dob
        member.age = age
        member.qualification = qualification
        member.occupation = occupation
        member.habit = habit
        if habit == True:
            member.habittype = habittype
        else:
            member.habittype = 'Null'
        member.save()

        house.added_no_of_members += 1

        if house.added_no_of_members == house.no_of_members:
            house.is_no_of_members_added = True
        
        house.save()

        return redirect('house_hold')
    
def house_details(request):
    if request.method == "POST":
        id = request.POST.get('id')

        house = House.objects.get(id=id)
        members = Members.objects.filter(house=house)
        children = Children.objects.all()
        pregnant = Pregnant.objects.all()
        patient = Patient.objects.all()

        context = {
            'house' : house,
            'members' : members,
            'children' : children,
            'pregnant' : pregnant,
            'patient' : patient,
        }

        return render(request, 'house_details.html', context)
    

def children(request):

    houses = House.objects.filter(child_onboard=True)

    context = {
        'houses' : houses,
    }

    return render(request, 'children.html', context)

def search_children(request):
    if request.method == "POST":
        house_no = request.POST.get('house_no') 

        houses = House.objects.filter(child_onboard=True, house_no=house_no)

        context = {
            'houses' : houses,
        }

        return render(request, 'children.html', context)

def add_children_request(request):
    if request.method == "POST":
        id = request.POST.get('id')
        house = House.objects.get(id=id)
        members = Members.objects.filter(house=house)
        return render(request, 'add_children.html', {'house':house, 'members':members})
    
def add_children(request):
    if request.method == "POST":
        member_id = request.POST.get('id')
        if request.POST.get('delivery'):
            delivery = True
        else:
            delivery = False
        if request.POST.get('threemonth'):
            threemonth = True
        else:
            threemonth = False
        if request.POST.get('sixmonth'):
            sixmonth = True
        else:
            sixmonth = False
        if request.POST.get('oneyear'):
            oneyear = True
        else:
            oneyear = False
        if request.POST.get('fiveyear'):
            fiveyear = True
        else:
            fiveyear = False
        if request.POST.get('tenyear'):
            tenyear = True
        else:
            tenyear = False
        if request.POST.get('fifteenyear'):
            fifteenyear = True
        else:
            fifteenyear = False
        if request.POST.get('reason'):
            reason = request.POST.get('reason')
        else:
            reason = 'Null'


        member = Members.objects.get(id=member_id)

        # child = Children(member=member)
        try:
            child = Children.objects.get(member=member)
        except Children.DoesNotExist:
            child = Children(member=member)
        child.delivery = delivery
        child.threemonth = threemonth
        child.sixmonth = sixmonth
        child.oneyear = oneyear
        child.fiveyear = fiveyear
        child.tenyear = tenyear
        child.fifteenyear = fifteenyear
        child.reason = reason
        child.save()

        house = House.objects.get(id=member.house.id)

        house.added_child_cound += 1

        if house.added_child_cound == house.child_cound:
            house.is_child_added = True
        
        house.save()
        

        return redirect('children')

def pregnant(request):

    houses = House.objects.filter(pregnant_onboard=True)

    context = {
        'houses' : houses,
    }

    return render(request, 'pregnant.html', context)

def search_pregnant(request):
    if request.method == "POST":
        house_no = request.POST.get('house_no')

        houses = House.objects.filter(pregnant_onboard=True, house_no=house_no)

        context = {
            'houses' : houses,
        }

        return render(request, 'pregnant.html', context)

def add_pregnant_request(request):
    if request.method == "POST":
        id = request.POST.get('id')
        house = House.objects.get(id=id)
        members = Members.objects.filter(house=house)
        return render(request, 'add_pregnant.html', {'house':house, 'members':members})
    
def add_pregnant(request):
    if request.method == "POST":
        member_id = request.POST.get('id')
        pregnancyMonths = request.POST.get('pregnancyMonths')
        month1_weight = bool(request.POST.get('month1_weight'))

        member = Members.objects.get(id=member_id)

        # pregnant = Pregnant(member=member)

        try:
            pregnant = Pregnant.objects.get(member=member)
        except Pregnant.DoesNotExist:
            pregnant = Pregnant(member=member)

        pregnant.pregnancy_months = pregnancyMonths
        pregnant.month1_weight = bool(request.POST.get('month1_weight'))
        pregnant.month1_bp = bool(request.POST.get('month1_bp'))
        pregnant.month1_hr = bool(request.POST.get('month1_hr'))
        pregnant.month2_weight = bool(request.POST.get('month2_weight'))
        pregnant.month2_bp = bool(request.POST.get('month2_bp'))
        pregnant.month2_hr = bool(request.POST.get('month2_hr'))
        pregnant.month3_weight = bool(request.POST.get('month3_weight'))
        pregnant.month3_bp = bool(request.POST.get('month3_bp'))
        pregnant.month3_hr = bool(request.POST.get('month3_hr'))
        pregnant.month4_weight = bool(request.POST.get('month4_weight'))
        pregnant.month4_bp = bool(request.POST.get('month4_bp'))
        pregnant.month4_hr = bool(request.POST.get('month4_hr'))
        pregnant.month5_weight = bool(request.POST.get('month5_weight'))
        pregnant.month5_bp = bool(request.POST.get('month5_bp'))
        pregnant.month5_hr = bool(request.POST.get('month5_hr'))
        pregnant.month6_weight = bool(request.POST.get('month6_weight'))
        pregnant.month6_bp = bool(request.POST.get('month6_bp'))
        pregnant.month6_hr = bool(request.POST.get('month6_hr'))
        pregnant.month7_weight = bool(request.POST.get('month7_weight'))
        pregnant.month7_bp = bool(request.POST.get('month7_bp'))
        pregnant.month7_hr = bool(request.POST.get('month7_hr'))
        pregnant.month8_weight = bool(request.POST.get('month8_weight'))
        pregnant.month8_bp = bool(request.POST.get('month8_bp'))
        pregnant.month8_hr = bool(request.POST.get('month8_hr'))
        pregnant.month9_weight = bool(request.POST.get('month9_weight'))
        pregnant.month9_bp = bool(request.POST.get('month9_bp'))
        pregnant.month9_hr = bool(request.POST.get('month9_hr'))
        pregnant.month10_weight = bool(request.POST.get('month10_weight'))
        pregnant.month10_bp = bool(request.POST.get('month10_bp'))
        pregnant.month10_hr = bool(request.POST.get('month10_hr'))
        pregnant.save()

        house = House.objects.get(id=member.house.id)

        house.added_pregnant_cound += 1

        if house.added_pregnant_cound == house.pregnant_cound:
            house.is_pregnant_added = True
        
        house.save()
        

        return redirect('pregnant')

def patient(request):
    houses = House.objects.filter(user=request.user,child_onboard=True)

    context = {
        'houses' : houses,
    }

    return render(request, 'patient.html', context)

def search_patient(request):
    if request.method == "POST":
        house_no = request.POST.get('house_no')

        houses = House.objects.filter(user=request.user,child_onboard=True, house_no=house_no)

        context = {
            'houses' : houses,
        }

        return render(request, 'patient.html', context)

def add_patient_request(request):
    if request.method == "POST":
        id = request.POST.get('id')
        house = House.objects.get(id=id)
        members = Members.objects.filter(house=house)
        return render(request, 'add_patient.html', {'house':house, 'members':members})
    
def add_patient(request):
    if request.method == "POST":
        member_id = request.POST.get('id')
        disease_details = request.POST.get('disease_details')
        pain = bool(request.POST.get('pain'))
        disease = bool(request.POST.get('disease'))

        member = Members.objects.get(id=member_id)

        # patient = Patient(member=member)
        try:
            patient = Patient.objects.get(member=member)
        except Patient.DoesNotExist:
            patient = Patient(member=member)
        patient.disease_details = disease_details
        patient.pain = pain
        patient.disease = disease
        patient.save()

        house = House.objects.get(id=member.house.id)

        house.added_patients_cound += 1

        if house.added_patients_cound == house.patients_cound:
            house.is_patients_added = True
        
        house.save()

        return redirect('patient')
    

def edit_household(request):
    if request.method == "POST":
        id = request.POST.get('id')
        section = request.POST.get('section')    

        request.session['household_id'] = {
            'id': id,
        }

        if section == 'pregnant':
            return redirect('edit_pregnant')

        elif section == 'patient':
            return redirect('edit_patient')

        elif section == 'children':
            return redirect('edit_children')

        else:
            pass


def edit_pregnant(request):

    house_mem_id = request.session.pop('household_id', None)
    if house_mem_id:
            # Extract data
        id = house_mem_id.get('id')

    pregnant = Pregnant.objects.get(id=id)

    context = {
        'pregnant' : pregnant,
    }

    return render(request, 'edit_pregnant.html', context)

def edit_patient(request):

    house_mem_id = request.session.pop('household_id', None)
    if house_mem_id:
            # Extract data
        id = house_mem_id.get('id')
        patient = Patient.objects.get(id=id)

    return render(request, 'edit_patient.html', {'patient':patient})

def edit_children(request):

    house_mem_id = request.session.pop('household_id', None)
    if house_mem_id:
            # Extract data
        id = house_mem_id.get('id')
        child = Children.objects.get(id=id)

    return render(request, 'edit_children.html', {'child':child})



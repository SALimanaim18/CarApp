from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Car, Client, Privacy, Ads
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.core.management import call_command

# installed rate limit
from django_ratelimit.decorators import ratelimit

import random

# Home page
def index(request):
    allcars = Car.objects.all().filter(vehicle_type="Car")
    total_vehicles = allcars.count()
    context = {'allcars': allcars, 'total_vehicles': total_vehicles}
    return render(request, 'index-3.html', context)

# list all cars on the used car page
def listing_classic(request):
    allcars = Car.objects.all()

    paginator = Paginator(allcars, 8)  # Show 8 contacts per page.

    page_number = request.GET.get('page')
    allcars = paginator.get_page(page_number)
    total_vehicles = Car.objects.count()
    context = {'allcars': allcars, 'total_vehicles': total_vehicles}
    return render(request, 'listing-classic.html', context)

# display car details
def listing_detail(request, myid):
    car = Car.objects.filter(id=myid)

    otp_verified = request.session.get('otp_verified', False)

    context = {'car': car[0], 'otp_verified': otp_verified}
    return render(request, 'listing-detail.html', context)

# search page function
def search(request):
    if request.method == 'GET':
        car_city = request.GET.get('city')
        vehicle_type = request.GET.get('vehicle_type')
        slider_range = request.GET.get('slider')
        range_list = slider_range.split(",")
        min = range_list[0]
        max = range_list[1]
        price_result = Car.objects.filter(expected_selling_price__range=(min, max))

        allcars = Car.objects.all()

        if car_city == "Select Location" and vehicle_type == "Select Vehicle Type":
            result = Car.objects.all()
        elif car_city == "Select Location":
            result = Car.objects.all().filter(vehicle_type=vehicle_type)
        elif vehicle_type == "Select Vehicle Type":
            result = Car.objects.all().filter(car_city=car_city)
        else:
            result = Car.objects.all().filter(car_city=car_city, vehicle_type=vehicle_type)

        final_dict = result & price_result

        total_vehicles = len(final_dict)
        context = {'result': final_dict, 'allcars': allcars, 'total_vehicles': total_vehicles}
        return render(request, 'search.html', context)

# All cars sorting by price
def sort(request):
    if request.method == 'GET':
        sort = request.GET.get('sort')
        sorted = Car.objects.all()
        low_to_high=None
        if sort == "Price (low to high)":
            sorted = Car.objects.order_by("expected_selling_price")
            low_to_high = True
        elif sort == "Price (high to low)":
            sorted = Car.objects.order_by("-expected_selling_price")
            low_to_high = False

        total_vehicles = sorted.count()
        allcars = Car.objects.all()
        context = {'sorted': sorted, 'allcars': allcars, 'total_vehicles': total_vehicles, 'low_to_high': low_to_high}
        return render(request, 'sort.html', context)

#Search page sorting by price
def search_sort(request):
    if request.method == 'GET':
        sort = request.GET.get('sort')
        all_search_page_cars = request.session.get('allcars')

        if sort == "Price (low to high)":
            sorted = Car.objects.order_by("expected_selling_price")
        elif sort == "Price (high to low)":
            sorted = Car.objects.order_by("-expected_selling_price")

        total_vehicles = sorted.count()
        allcars = Car.objects.all()
        context = {'sorted': sorted, 'allcars': allcars, 'total_vehicles': total_vehicles}
        return render(request, 'sort.html', context)

# Add a Car
@login_required(login_url='/#loginModal')
def post_vehicle(request):
    if request.method == 'POST':
        car_title = request.POST['car_title']
        make_year = request.POST['make_year']
        make_month = request.POST['make_month']
        car_manufacturer = request.POST['car_manufacturer']
        car_model = request.POST['car_model']
        car_version = request.POST['car_version']
        car_color = request.POST['car_color']
        fuel_type = request.POST['fuel_type']
        transmission_type = request.POST['transmission_type']
        car_owner = request.POST['car_owner']
        kilometer_driven = request.POST['kilometer_driven']
        expected_selling_price = request.POST['expected_selling_price']
        registration_type = request.POST['registration_type']
        insurance_type = request.POST['insurance_type']
        registration_number = request.POST['registration_number']
        car_description = request.POST['car_description']
        car_photo = request.FILES['car_photo']
        car_owner_phone_number = request.POST['car_owner_phone_number']
        car_city = request.POST['car_city']
        car_owner_name = request.POST['car_owner_name']
        user = request.user

        if not kilometer_driven.isnumeric():
            kilometer_driven = None
        if not make_year.isnumeric():
            make_year = None
        if not expected_selling_price.isnumeric():
            expected_selling_price = None
        if not car_owner_phone_number.isnumeric():
            car_owner_phone_number = None

        car = Car(
            car_title=car_title,
            make_year=make_year,
            make_month=make_month,
            car_manufacturer=car_manufacturer,
            car_model=car_model,
            car_version=car_version,
            car_color=car_color,
            fuel_type=fuel_type,
            transmission_type=transmission_type,
            car_owner=car_owner,
            kilometer_driven=kilometer_driven,
            expected_selling_price=expected_selling_price,
            registration_type=registration_type,
            insurance_type=insurance_type,
            registration_number=registration_number,
            car_description=car_description,
            car_photo=car_photo,
            car_owner_phone_number=car_owner_phone_number,
            car_city=car_city,
            car_owner_name=car_owner_name,
            user=user,
        )

        car.save()

    return render(request, 'post-vehicle.html', {})

#Display users vehicles
@login_required(login_url='/#loginModal')
def my_vehicles(request):
    cars = Car.objects.filter(user=request.user)
    context = {'cars': cars}
    return render(request, 'my-vehicles.html', context)

#Delete user vehicle
@login_required(login_url='/#loginModal')
def delete_vehicles(request, myid):
    obj = get_object_or_404(Car, id=myid)
    try:
        call_command('dbbackup')
    except:
        pass
    if request.method == "POST":
        obj.delete()
        return redirect('/my-vehicles.html')
    return render(request, 'my-vehicles.html', {})

#User profile setting
@login_required(login_url='/#loginModal')
def profile_settings(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, 'Please retry for password change')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile-settings.html', {'form': form})

#About us page
def about_us(request):
    return render(request, 'about-us.html', {})

#Signup page
@ratelimit(key='ip', rate='10/h', block=True)
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters")
            signup_url = request.META['HTTP_REFERER'] + "#signupModal"
            return redirect(signup_url)
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            signup_url = request.META['HTTP_REFERER'] + "#signupModal"
            return redirect(signup_url)
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            signup_url = request.META['HTTP_REFERER'] + "#signupModal"
            return redirect(signup_url)
        
        if pass1 != pass2:
            messages.error(request, "Password do Not match")
            signup_url = request.META['HTTP_REFERER'] + "#signupModal"
            return redirect(signup_url)
        
        if len(pass1) < 6:
            messages.error(request, "Password length must be greater than 6")
            signup_url = request.META['HTTP_REFERER'] + "#signupModal"
            return redirect(signup_url)

        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        messages.success(request, "Your account has been created")
        
        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, "Invalid Credentials")
            login_url = request.META['HTTP_REFERER'] + "#loginModal"
            return redirect(login_url)

        return redirect(request.META['HTTP_REFERER'])
    
    else:
        return HttpResponse('404- Not Found')

#User Login Modal
@ratelimit(key='ip', rate='10/h', block=True)
def login_model(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        
        user = authenticate(username=loginusername, password=loginpass)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, "Invalid Credentials")
            login_url = request.META['HTTP_REFERER'] + "#loginModal"
            return redirect(login_url)
    return HttpResponse("404- Not Found")

#User Logout Modal
def logout_model(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect(request.META['HTTP_REFERER'])

# Privacy Page
def privacy(request):
    policy = Privacy.objects.all()
    context = {'policy': policy[0]}
    return render(request, 'privacy.html', context)

# Submit phone number to access details
@ratelimit(key='ip', rate='10/h', block=True)
def submit_number(request):
    phone_number = request.session.get('session_phone_number')
    if phone_number is None:
        return HttpResponse("Numéro de téléphone non trouvé dans la session", status=400)
    try:
        phone_number = int(phone_number)
    except ValueError:
        return HttpResponse("Format de numéro de téléphone invalide", status=400)
    
    if Client.objects.filter(phone_number=phone_number).exists():
        request.session['otp_verified'] = True
        rel_url = 'listing-detail.html/' + str(request.session.get('session_otp_car_id', '')) + '/'
        return redirect(rel_url)
    else:
        request.session['session_otp'] = generate_otp_message(request)
        return HttpResponse("OTP généré et envoyé", status=200)

#Submit the OTP
def submit_otp(request):
    if request.method == 'POST':
        get_otp = request.POST.get('get_otp')
        if 'session_otp' not in request.session:
            return HttpResponse("OTP non trouvé dans la session", status=400)
        if int(get_otp) == int(request.session['session_otp']):
            client = Client(name=request.session['session_phone_name'], phone_number=int(request.session['session_phone_number']))
            client.save()
            request.session['otp_verified'] = True

            rel_url = 'listing-detail.html/' + str(request.session['session_otp_car_id'])
            return redirect(rel_url)
        else:
            r_url = 'listing-detail.html/' + str(request.session['session_otp_car_id']) + '/#submit_otp'
            return redirect(r_url)
        
    return HttpResponse("404- Details Not Found for submit otp")

# Disclaimer page
def disclaimer(request):
    return render(request, 'Disclaimer.html')

# Importez les modules appropriés

def definir_numero_telephone(request):
    if request.method == 'POST':
        numero_telephone = request.POST.get('numero_telephone')
        if numero_telephone:
            request.session['session_phone_number'] = numero_telephone
            request.session['session_phone_name'] = request.POST.get('name', '')  # Assuming you get the name from the form
            return redirect('submit_number')  # Redirigez vers la vue de soumission du numéro de téléphone
        return HttpResponse("Le numéro de téléphone est requis", status=400)
    return render(request, 'definir_numero_telephone.html')

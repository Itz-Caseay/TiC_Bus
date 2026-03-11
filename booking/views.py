from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
# from .forms import BookingForm
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .models import User, UserProfile, Agency, Bus, Route, Booking
from django.contrib import messages

# Create your views here.
@login_required(login_url='login')
def index(request):

    total_agencies = Agency.objects.count()
    total_buses = Bus.objects.count()
    total_bookings = Booking.objects.count()
    total_destinations = Route.objects.count()

    # Count buses and routes for each agency
    agencies = Agency.objects.annotate(
        unique_agency_total_bus=Count('buses'),
        total_routes=Count('buses__route')
    )

    context = {
        'total_agencies': total_agencies,
        'total_buses': total_buses,
        'total_destinations': total_destinations,
        'total_bookings': total_bookings,
        'agencies': agencies,
    }

    return render(request, 'pages/index.html', context)

def agency_detail(request, agency_id):
    agency = get_object_or_404(Agency, id=agency_id)
    buses = agency.buses.all()
    routes = Route.objects.filter(bus__agency=agency)
    unique_agency_total_bus = buses.count()
    
    return render(request, "pages/agency-detail.html", {
        "agency": agency,
        "buses": buses,
        "routes": routes,
        "unique_agency_total_bus": unique_agency_total_bus
    })

# User logging system

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged In")
                return redirect('index')
            
            else:
                messages.error(request, "Invalid Credentials")
                return redirect('login')
        
        except Exception as e:
            
            messages.error(request, {'error':e})
    return render(request, "auth/login.html")

# User registration system

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password == password2:
            if User.objects.filter(email=email, username=username).exists():
                messages.error(request, "Username or Email already taken use another email")
                return redirect('signup')
            
            else:
                user = User.objects.create_user(username=username, fullname=fullname, email=email, password=password)
                login(request, user)
                messages.success(request, "Account successfully created")
                profile = UserProfile.objects.create(user=user)
                profile.save()
                user.save()
                return redirect('index')
            
        else:
            messages.error(request, "Passwords donot match retry")
            return redirect('signup')
        
    return render(request, 'auth/signup.html')

# User logout system
@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request, "Logout Successful")
    return redirect('login')


# @login_required(login_url='login')
# def book_ticket(request, route_id):
#     route = get_object_or_404(Route, id=route_id)

#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.user = request.user
#             booking.route = route
#             booking.save()
#             return redirect('my_bookings')

#     else:
#         form = BookingForm()

#     return render(request, 'pages/book_ticket.html', {'form': form, 'route': route})


@login_required(login_url='login')
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'pages/my_bookings.html', {'bookings': bookings})

@login_required(login_url='login')
def book_bus(request, route_id):

    route = get_object_or_404(Route, id=route_id)

    bus = route.bus

    if request.method == "POST":

        seat_number = request.POST.get("seat_number")

        Booking.objects.create(
            user=request.user,
            route=route,
            bus=bus,
            seat_number=seat_number
        )

        return redirect("dashboard")

    context = {
        "route": route,
        "bus": bus
    }

    return render(request, "pages/book_bus.html", context)
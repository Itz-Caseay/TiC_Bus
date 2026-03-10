from django.urls import path
from .views import index, login_user, logout_user, signup, my_bookings, agency_detail, book_bus

urlpatterns = [
    path('index/', index, name="index"),
    path('', login_user, name="login"),
    path('signup/', signup, name="signup"),
    path('logout/', logout_user, name="logout"),
    path('my-bookings/', my_bookings, name='my_bookings'),
    path('agency/<int:agency_id>/', agency_detail, name="agency_detail"),
    path("book/<int:route_id>/", book_bus, name="book_bus"),
]

from django.contrib import admin
from .models import User, Agency, Bus, Route, Booking, UserProfile

# Register your models here.
admin.site.register(User)
admin.site.register(Agency)
admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(Booking)
admin.site.register(UserProfile)
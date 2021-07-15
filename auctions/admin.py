from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Listings, Categories, User, Watchlists, Bid, Comments
# Register your models here.

#admin.site.register(User,UserAdmin)
admin.site.register(Listings)
admin.site.register(Categories)
admin.site.register(User)
admin.site.register(Watchlists)
admin.site.register(Bid)
admin.site.register(Comments)

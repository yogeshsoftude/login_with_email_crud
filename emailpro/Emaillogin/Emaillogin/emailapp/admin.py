from django.contrib import admin
from emailapp.models import User,user_datails
# from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(User)
admin.site.register(user_datails)

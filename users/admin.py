from django.contrib import admin
from .models import CustomUser,EmailVerification

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_active',
                    'is_staff', 'is_superuser', 'last_login','password','is_verified')    

admin.site.register(CustomUser) 
admin.site.register(EmailVerification) 
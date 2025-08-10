from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Doctor, Patient, User, Appointment, Prescription

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'user_type', 'is_staff', 'is_superuser') 
    list_filter = ('user_type', 'is_superuser')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    ) 
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type'),
        }),
    )

admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Prescription)
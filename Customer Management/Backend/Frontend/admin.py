from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(Customer)
admin.site.register(Staff)
admin.site.register(User_details)
admin.site.register(Product)
admin.site.register(Incentive)
admin.site.register(Bill)
admin.site.register(Catogery)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_superuser")
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("role", "phone_number", "dob", "new_pass")}),
    )


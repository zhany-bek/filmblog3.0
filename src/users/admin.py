from django.contrib import admin
from .models import Profile

# Register your models here.

# Profile tab admin model:
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'date_of_birth')
    readonly_fields = ('user_ID', 'first_name', 'last_name')
    
    def user_ID(self, obj):
        return obj.user.id
    user_ID.short_description = 'User ID'
    
    # Customize the order of fields in the admin form
    fieldsets = (
        (None, {'fields': ('user', 'user_ID', 'first_name', 'last_name', 'date_of_birth')}),
        (None, {'fields': ('profile_picture', 'bio',)}),
    )

admin.site.register(Profile, ProfileAdmin)
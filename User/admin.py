from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Contact, Tag, ContactSocialLink, ContactActivity

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_email_verified', 'date_joined')
    search_fields = ('username', 'email', 'company')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_email_verified')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Profile Info', {'fields': ('profile_image', 'phone_number', 'bio', 'company', 'job_title', 'timezone', 'is_email_verified')}),
    )

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'color')
    search_fields = ('name', 'user__username', 'user__email')
    list_filter = ('user',)

class ContactSocialLinkInline(admin.TabularInline):
    model = ContactSocialLink
    extra = 1

class ContactActivityInline(admin.TabularInline):
    model = ContactActivity
    extra = 0
    readonly_fields = ('created_at',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'email', 'phone_number', 'company', 'is_favorite')
    search_fields = ('name', 'first_name', 'last_name', 'email', 'phone_number', 'company', 'user__username')
    list_filter = ('is_favorite', 'is_archived', 'user')
    autocomplete_fields = ['user', 'tags']
    inlines = [ContactSocialLinkInline, ContactActivityInline]
    fieldsets = (
        ('Ownership', {'fields': ('user',)}),
        ('Core Details', {'fields': ('name', 'first_name', 'last_name', 'profile_image')}),
        ('Contact Info', {'fields': ('email', 'secondary_email', 'phone_number', 'secondary_phone', 'website')}),
        ('Professional', {'fields': ('company', 'job_title')}),
        ('Location', {'fields': ('address', 'city', 'state', 'country', 'postal_code')}),
        ('Extra', {'fields': ('birthday', 'notes', 'tags', 'is_favorite', 'is_archived')}),
    )
    
@admin.register(ContactActivity)
class ContactActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_type', 'contact', 'user', 'created_at')
    search_fields = ('contact__name', 'user__username')
    list_filter = ('activity_type', 'created_at')
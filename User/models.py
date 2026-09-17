from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    # AbstractUser provides first_name, last_name, email, password, is_staff, is_superuser, is_active, date_joined
    profile_image = models.ImageField(upload_to='avatars/users/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    is_email_verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email or self.username


class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    color = models.CharField(max_length=20, default='#7c3aed') # Default accent color
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'name')
        ordering = ['name']

    def __str__(self):
        return self.name


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    
    # Core identifying info (preserving backward compatibility for 'name' and 'phone_number')
    name = models.CharField(max_length=100) # Used as display_name / full name
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    
    # Contact details
    email = models.EmailField(null=True, blank=True)
    secondary_email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    secondary_phone = models.CharField(max_length=20, null=True, blank=True)
    
    # Professional
    profile_image = models.ImageField(upload_to='avatars/contacts/', null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    
    # Location
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    
    # Extra
    birthday = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    # Relationships & Status
    tags = models.ManyToManyField(Tag, blank=True, related_name='contacts')
    is_favorite = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_contacted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['user', 'name']),
            models.Index(fields=['user', 'is_favorite']),
            models.Index(fields=['user', 'company']),
        ]

    def __str__(self):
        return self.name


class ContactSocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('linkedin', 'LinkedIn'),
        ('github', 'GitHub'),
        ('twitter', 'Twitter/X'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('website', 'Personal Website'),
        ('other', 'Other'),
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('contact', 'platform', 'url')

    def __str__(self):
        return f"{self.contact.name} - {self.platform}"


class ContactActivity(models.Model):
    ACTIVITY_CHOICES = [
        ('created', 'Contact Created'),
        ('updated', 'Contact Updated'),
        ('favorite_added', 'Favorite Added'),
        ('favorite_removed', 'Favorite Removed'),
        ('imported', 'Contact Imported'),
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.activity_type} - {self.contact.name}"

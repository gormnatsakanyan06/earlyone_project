from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from smart_selects.db_fields import ChainedForeignKey
import uuid
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class Contact(models.Model):
    types= [("Customer", "Հաճախորդ"),
           ("Partner", "Գործընկեր"),
           ]
    type = models.CharField(max_length=20, choices=types)
    name = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    phone = models.CharField(max_length=80, unique=True, null=True)
    message = models.CharField(max_length=222)
    company = models.CharField(max_length=80,null=True)

    def __str__(self):
        return f"{self.get_type_display()} | {self.type} | {self.name} | {self.email} | {self.phone}"


class Category(models.Model):
    name = models.CharField(max_length=100) 
    slug = models.SlugField(unique=True)     
    svg_path = models.TextField()            
    tagline = models.CharField(max_length=255, blank=True)

    header_title = models.CharField(max_length=255, default="Seamless Connection")
    
    feature_1_title = models.CharField(max_length=100, blank=True)
    feature_1_desc = models.TextField(blank=True)
    
    feature_2_title = models.CharField(max_length=100, blank=True)
    feature_2_desc = models.TextField(blank=True)
    
    feature_3_title = models.CharField(max_length=100, blank=True)
    feature_3_desc = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Provider(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='providers')
    name = models.CharField(max_length=200) # e.g., "Ameria Bank"
    slug = models.SlugField(unique=True)     # e.g., "ameria"
    logo = models.ImageField(upload_to='providers/logos/')
    
    def __str__(self):
        return self.name

class Branch(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=100)    # e.g., "Sayat Nova Branch"
    slug = models.SlugField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.provider.name} - {self.name}"

class Action(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='actions')
    name = models.CharField(max_length=100) # e.g., "Card Service"
    slug = models.SlugField()
    icon_svg = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.provider.name} : {self.name}"


class QRCode(models.Model):
    text = models.TextField(unique=True)  
    image = models.ImageField(upload_to='media/qr_codes/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    
    # 1. Link directly to your new Category model instead of hardcoded choices
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="appointments"
    )

    # 2. Add a direct link to the Branch
    # This makes it much easier to see WHERE the appointment is 
    # without digging into the GenericForeignKey.
    branch = models.ForeignKey(
        Branch, 
        on_delete=models.CASCADE, 
        related_name="appointments",
        null=True
    )

    # 3. The Generic Relation (Points to the specific 'Action')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    service_action = GenericForeignKey('content_type', 'object_id')

    scheduled_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(null=True, blank=True)

    # QR Logic
    verification_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    qr_code = models.OneToOneField("QRCode", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        branch_name = self.branch.name if self.branch else "Unknown Branch"
        return f"{self.full_name} | {branch_name} | {self.scheduled_at.strftime('%Y-%m-%d %H:%M')}"





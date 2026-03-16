from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Maharashtra Districts List
MAHARASHTRA_DISTRICTS = [
    ('ahmednagar', 'Ahmednagar'),
    ('akola', 'Akola'),
    ('amravati', 'Amravati'),
    ('aurangabad', 'Aurangabad'),
    ('beed', 'Beed'),
    ('bidar', 'Bidar'),
    ('buldhana', 'Buldhana'),
    ('chandrapur', 'Chandrapur'),
    ('dhule', 'Dhule'),
    ('gadchiroli', 'Gadchiroli'),
    ('gondia', 'Gondia'),
    ('hingoli', 'Hingoli'),
    ('jalgaon', 'Jalgaon'),
    ('jalna', 'Jalna'),
    ('kolhapur', 'Kolhapur'),
    ('latur', 'Latur'),
    ('mumbai_city', 'Mumbai City'),
    ('mumbai_suburban', 'Mumbai Suburban'),
    ('nagpur', 'Nagpur'),
    ('nanded', 'Nanded'),
    ('nandurbar', 'Nandurbar'),
    ('nashik', 'Nashik'),
    ('osmanabad', 'Osmanabad'),
    ('palghar', 'Palghar'),
    ('parbhani', 'Parbhani'),
    ('pune', 'Pune'),
    ('raigad', 'Raigad'),
    ('ratnagiri', 'Ratnagiri'),
    ('sangli', 'Sangli'),
    ('satara', 'Satara'),
    ('sindhudurg', 'Sindhudurg'),
    ('solapur', 'Solapur'),
    ('thane', 'Thane'),
    ('wardha', 'Wardha'),
    ('washim', 'Washim'),
    ('yavatmal', 'Yavatmal'),
]

class FarmerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Farmer(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        ('labor', 'Labor'),
        ('coordinator', 'Coordinator'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='farmer')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True, null=True, blank=True)
    
    # For coordinators - assigned region/district
    assigned_district = models.CharField(max_length=50, choices=MAHARASHTRA_DISTRICTS, null=True, blank=True)
    
    # Common fields
    village = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=50, choices=MAHARASHTRA_DISTRICTS, null=True, blank=True)
    farm_location = models.CharField(max_length=255, null=True, blank=True)
    farm_size = models.FloatField(null=True, blank=True)
    crop_type = models.CharField(max_length=100, null=True, blank=True)
    
    SOIL_CHOICES = [
        ('clay', 'Clay'),
        ('sandy', 'Sandy'),
        ('loamy', 'Loamy'),
        ('silt', 'Silt'),
        ('peaty', 'Peaty'),
        ('chalky', 'Chalky'),
    ]
    
    IRRIGATION_CHOICES = [
        ('drip', 'Drip Irrigation'),
        ('sprinkler', 'Sprinkler'),
        ('flood', 'Flood Irrigation'),
        ('manual', 'Manual'),
        ('none', 'Rain-fed Only'),
    ]

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    soil_type = models.CharField(max_length=50, choices=SOIL_CHOICES, null=True, blank=True)
    irrigation_type = models.CharField(max_length=50, choices=IRRIGATION_CHOICES, null=True, blank=True)
    planting_date = models.DateField(null=True, blank=True)
    crop_variety = models.CharField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = FarmerManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    def __str__(self):
        return self.email

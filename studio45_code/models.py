from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.core.validators import RegexValidator
from django_countries.fields import CountryField



def fileLocation(instance,data):
    return f'{instance}/1/document/{data}'


ROLES = ((0, 'Admin'), (1, 'User'), )

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
)

LEVEL = (
    ('Recreational', 'Recreational'),
    ('Amateur', 'Amateur'),
    ('Professional', 'Professional'),
)
    

class User(AbstractBaseUser, PermissionsMixin):
    role = models.IntegerField(choices=ROLES, default=1)
    email = models.EmailField(_('email address'),unique=True)
    username = models.CharField(_('username'), max_length=100, unique=False)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=200,blank=True,null=True)
    last_name = models.CharField(max_length=200,blank=True,null=True)
    profile_image_update = models.ImageField(upload_to='Profile_images/', null=True,blank=True)
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=100, blank=True)    
    name = models.CharField(max_length=200,blank=True,null=True)
    mobile_number = models.CharField(max_length=20,blank=True,null=True)
    primary_number = models.CharField(max_length=20,blank=True)
    mobile_number_verified =  models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    address = models.TextField(max_length=200,blank=True)
    city = models.CharField(max_length=120,blank=True)
    state = models.CharField(max_length=120,blank=True)
    country = models.CharField(max_length=120,null=True,blank=True)
    forget_password_token = models.CharField(max_length=100,blank=True,null=True)
    mobile_verify_token = models.CharField(max_length=100,blank=True)
    email_verify_token = models.CharField(max_length=100,blank=True)
    status = models.BooleanField(default=False)
    is_block = models.BooleanField(default=True)
    about_me = models.TextField(max_length=255,blank=True)
    age = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    martial_art_style = models.CharField(max_length=120,null=True,blank=True)
    competition_level = models.CharField(choices=LEVEL,max_length=120,blank=True,null=True)
    zip_code = models.IntegerField(blank=True,null=True)
    gender = models.CharField(max_length=255, choices=GENDER, blank=True,null=True)
    created_at = models.DateField(auto_now_add=True, editable=False)
    updated_at =models.DateTimeField(auto_now=True, editable=False)
    token_expire_time = models.DateTimeField(null=True, blank=True)
    
   

    # USERNAME_FIELD = 'mobile_number'
    # REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_number']

    objects = UserManager()

    # @property
    # def highlighted_numbers(self):
    #     return self.numbers_set.filter(highlight=True).order_by('-highlight_expiry_date')

    def __str__(self):
        return self.email





class Add_Blog(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog-images/', null=True,blank=True)
    description =  models.TextField()
    status = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True, editable=False)


class Contact(models.Model):
    email = models.EmailField(max_length=255,null=True,blank=True)
    phone = models.CharField(max_length=15,null=True,blank=True)
    address =  models.TextField(null=True,blank=True)



# -----------old_events_table------------------------

# class Events(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     image = models.ImageField(upload_to='Event-images/', null=True,blank=True)
#     description = models.TextField(default=None, blank=True, null=True)
#     start_date = models.DateField(default=None,null=True, blank=True)
#     end_date = models.DateField(default=None,null=True, blank=True)
#     location = models.CharField(max_length=255)
#     status = models.BooleanField(default=False)
#     modified = models.DateTimeField(auto_now=True, editable=False)
#     created = models.DateTimeField(auto_now_add=True, editable=False)



class Events(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255,blank=True,null=True)
    zip_code = models.IntegerField(blank=True,null=True)
    country = CountryField()
    time = models.TimeField(null=True,blank=True,default=None)
    organizer_first_name = models.CharField(max_length=255) 
    organizer_last_name = models.CharField(max_length=255)
    organizer_phone_number = models.IntegerField()
    organizer_email  = models.EmailField(max_length=255)
    organizer_social_media_links  = models.CharField(max_length=255)
    does_this_event_accept_foreign_participants  = models.BooleanField(max_length=255)
    instructions_for_the_event   = models.CharField(max_length=255)
    related_associations_or_organizations   = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='Event_images/', null=True,blank=True)
    description = models.TextField(default=None)
    start_date = models.DateField(default=None,null=True, blank=True)
    end_date = models.DateField(default=None,null=True, blank=True)
    # location = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateField(auto_now=True, editable=False,null=True,blank=True)
    updated_at =models.DateField(auto_now=True, editable=False,null=True,blank=True)
    is_approved = models.BooleanField(default=False)



class UserContact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "contact"
        verbose_name_plural = "UserContact"      



class SeminarInformation(models.Model):
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zip_code = models.IntegerField()
    country = CountryField()
    organizer_first_name = models.CharField(max_length=255) 
    organizer_last_name = models.CharField(max_length=255)
    organizer_phone_number = models.IntegerField()
    organizer_email  = models.EmailField(max_length=255)
    image = models.ImageField(upload_to='Seminar_images/', null=True,blank=True)
    organizer_social_media_links  = models.CharField(max_length=255)
    does_this_event_accept_foreign_participants  = models.BooleanField(default=False)
    why_is_this_seminar_only_open_to_this_group_of_people  = models.CharField(max_length=255,null=True,blank=True)
    cost_of_seminar = models.CharField(max_length=255)
    start_date = models.DateField(default=None,null=True, blank=True)
    end_date = models.DateField(default=None,null=True, blank=True)
    # dates_of_seminar = models.CharField(max_length=255)
    special_instructions = models.CharField(max_length=255)
    details = models.CharField(max_length=255)
    created_at = models.DateField(auto_now=True, editable=False,null=True,blank=True)
    updated_at =models.DateField(auto_now=True, editable=False,null=True,blank=True)
    is_approved = models.BooleanField(default=False)           




class SchoolGym(models.Model):
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zip_code = models.IntegerField()
    country = CountryField()
    owner_first_name = models.CharField(max_length=255) 
    owner_last_name = models.CharField(max_length=255)
    owner_phone_number = models.IntegerField()
    owner_email  = models.EmailField(max_length=255)
    price_min_ranges  = models.IntegerField()
    price_max_ranges  = models.IntegerField()
    days_of_operation  = models.IntegerField()
    hours_of_operation  = models.CharField(max_length=255)
    introduction  = models.CharField(max_length=255)
    owner_social_media_links = models.CharField(max_length=255)
    special_instructions = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True, editable=False,null=True,blank=True)
    updated_at =models.DateField(auto_now=True, editable=False,null=True,blank=True)
    image = models.ImageField(upload_to='schoolym_images/', null=True,blank=True) 


EVENTS_TYPE = (
    ('Events', 'Events'),
    ('SeminarInformation', 'SeminarInformation'),
    ('SchoolGym', 'SchoolGym'),
)

class all_events_details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    events = models.ForeignKey(Events, on_delete=models.CASCADE,null=True,blank=True)
    seminarnformation = models.ForeignKey(SeminarInformation, on_delete=models.CASCADE,null=True,blank=True)
    schoolgym = models.ForeignKey(SchoolGym, on_delete=models.CASCADE,null=True,blank=True)
    type = models.CharField(max_length=255,choices=EVENTS_TYPE)
    created_at = models.DateField(auto_now=True, editable=False,null=True,blank=True)
    updated_at =models.DateField(auto_now=True, editable=False,null=True,blank=True) 



class Pages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,null=True,blank=True)
    contant = models.TextField()
    created_at = models.DateField(auto_now=True, editable=False,null=True,blank=True)
    updated_at =models.DateField(auto_now=True, editable=False,null=True,blank=True)
    



class Industry(models.Model):
    Industry = models.CharField(max_length=255,null=True,blank=True)
    newfile = models.CharField(max_length=255,null=True,blank=True)
    


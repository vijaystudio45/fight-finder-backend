from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models
import mapbox


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
    username = models.CharField(_('username'), max_length=100, unique=True)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=200,blank=True,null=True)
    last_name = models.CharField(max_length=200,blank=True,null=True)
    profile_image_update = models.ImageField(upload_to='Profile_images/',blank=True, null=True)
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
    competition_level = models.CharField(choices=LEVEL,max_length=120,blank=True,null=True)
    zip_code = models.IntegerField(blank=True,null=True)
    gender = models.CharField(max_length=255, choices=GENDER, blank=True,null=True)
    created_at = models.DateField(auto_now_add=True, editable=False)
    updated_at =models.DateTimeField(auto_now=True, editable=False)
    token_expire_time = models.DateTimeField(null=True, blank=True)
    Social_media_links = models.CharField(null=True,blank=True,max_length=255)
    
    
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_number']

    objects = UserManager()

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



class Tag(models.Model):
    tag_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)



class Events(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=2000,blank=True,null=True)
    zip_code = models.CharField(max_length=200,blank=True,null=True)
    # country = CountryField(blank=True,null=True)
    contact_title = models.CharField(max_length=2000,blank=True,null=True)
    event_link = models.CharField(max_length=700,default="")
    comments_by_data_entry_associate = models.CharField(max_length=2000,blank=True,null=True)
    is_more_information_coming_soon = models.CharField(max_length=2000,blank=True,null=True)
    event_flyer_material = models.CharField(max_length=2000,blank=True,null=True)
    online_registration_link = models.CharField(max_length=2000,default="",blank=True,null=True)
    country = models.CharField(max_length=2000,blank=True,null=True)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    time = models.TextField(null=True,blank=True,default=None)
    contact_first_name = models.CharField(max_length=2000) 
    contact_last_name = models.CharField(max_length=2000)
    contact_phone_number = models.CharField(max_length=20,blank=True,null=True)
    contact_email  = models.CharField(max_length=2000)
    contact_social_media_links  = models.CharField(max_length=2000)
    does_this_event_accept_foreign_participants  = models.CharField(max_length=2000, null=True,blank=True)
    instructions_for_the_event   = models.CharField(max_length=2000)
    related_associations_or_organizations   = models.CharField(max_length=2000,null=True,blank=True)
    title = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='Event_images/', null=True,blank=True)
    city = models.CharField(max_length=2000,null=True, blank=True)
    start_date = models.DateField(default=None,null=True, blank=True)
    end_date = models.DateField(default=None,null=True, blank=True)
    # location = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateField(auto_now=True, editable=False,null=True,blank=True)
    updated_at =models.DateField(auto_now=True, editable=False,null=True,blank=True)
    is_approved = models.BooleanField(default=False)
    online_only = models.CharField(max_length=120,default=False)
    martial_art_style = models.CharField(max_length=120,null=True,blank=True)
    website = models.CharField(max_length=120,default="",blank=True,null=True)
    tags = models.ManyToManyField(Tag,null=True, blank=True)
    point = models.PointField(null=True, blank=True)
    event_participants = models.TextField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            try:
                geocoder = mapbox.Geocoder(access_token="pk.eyJ1Ijoic2Znb256YWxlejIwNiIsImEiOiJjbGRsNTE5OGswdHh0M3Btc2RuODVmM2F1In0.Xnkdku_W_aclNetMgvK-Og")
                response = geocoder.forward(self.address)
                if response.status_code == 200 and response.geojson()['features']:
                    feature = response.geojson()['features'][0]
                    self.latitude = feature['center'][1]
                    self.longitude = feature['center'][0]
                    self.point = Point(self.latitude, self.longitude)
            except Exception as e:
                print(e)
        super(Events, self).save(*args, **kwargs)


    # def save(self, *args, **kwargs):
    #     geocoder = mapbox.Geocoder(access_token=("pk.eyJ1Ijoic2Znb256YWxlejIwNiIsImEiOiJjbGRsNTE5OGswdHh0M3Btc2RuODVmM2F1In0.Xnkdku_W_aclNetMgvK-Og"))
    #     response = geocoder.forward(self.address)
    #     if response.status_code == 200 and response.geojson()['features']:
    #         feature = response.geojson()['features'][0]
    #         self.latitude = feature['center'][1]
    #         self.longitude = feature['center'][0]
    #         self.point = Point(self.latitude,self.longitude)
    #     super(Events, self).save(*args, **kwargs)



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
    title = models.CharField(max_length=2000)
    address = models.CharField(max_length=2000,blank=True,null=True)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    zip_code = models.CharField(max_length=2000,blank=True,null=True)
    country = models.CharField(max_length=2000,blank=True,null=True)
    first_name = models.CharField(max_length=2000) 
    last_name = models.CharField(max_length=2000)
    phone_number = models.CharField(max_length=20)
    organizer_email  = models.EmailField(max_length=255)
    image = models.ImageField(upload_to='Seminar_images/', null=True,blank=True)
    social_media_links  = models.CharField(max_length=2000)
    does_this_event_accept_foreign_participants  = models.CharField(max_length=2000,default=False)
    why_is_this_seminar_only_open_to_this_group_of_people  = models.CharField(max_length=2000,null=True,blank=True)
    cost_of_seminar = models.CharField(max_length=2000)
    start_date = models.DateField(default=None,null=True, blank=True)
    end_date = models.DateField(default=None,null=True, blank=True)
    # dates_of_seminar = models.CharField(max_length=255)
    special_instructions = models.CharField(max_length=2000)
    online_registration_link = models.CharField(max_length=2000,default="",null=True,blank=True)
    details = models.CharField(max_length=2000)
    created_at = models.DateField(auto_now=True, editable=False,null=True,blank=True)
    updated_at =models.DateField(auto_now=True, editable=False,null=True,blank=True)
    is_approved = models.BooleanField(default=False)    
    online_only = models.CharField(max_length=2000,default=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    martial_art_style = models.CharField(max_length=120,null=True,blank=True)
    website = models.CharField(max_length=2000,default="",blank=True,null=True)     
    event_flyer_material = models.CharField(max_length=2000,blank=True,null=True)  
    event_link = models.CharField(max_length=2000,default="",blank=True,null=True)
    comments_by_data_entry_associate = models.CharField(max_length=2000,blank=True,null=True)
    is_more_information_coming_soon = models.CharField(max_length=2000,blank=True,null=True)
    tags = models.ManyToManyField(Tag)
    point = models.PointField(null=True, blank=True)
    seminar_participants = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=2000,null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            try:
                geocoder = mapbox.Geocoder(access_token="pk.eyJ1Ijoic2Znb256YWxlejIwNiIsImEiOiJjbGRsNTE5OGswdHh0M3Btc2RuODVmM2F1In0.Xnkdku_W_aclNetMgvK-Og")
                response = geocoder.forward(self.address)
                if response.status_code == 200 and response.geojson()['features']:
                    feature = response.geojson()['features'][0]
                    self.latitude = feature['center'][1]
                    self.longitude = feature['center'][0]
                    self.point = Point(self.latitude, self.longitude)
            except Exception as e:
                print(e)
        super(SeminarInformation, self).save(*args, **kwargs)



class SchoolGym(models.Model):
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    zip_code = models.CharField(max_length=2000,blank=True,null=True)
    country = models.CharField(max_length=255,blank=True,null=True)
    owner_first_name = models.CharField(max_length=255) 
    owner_last_name = models.CharField(max_length=255)
    owner_phone_number = models.CharField(max_length=20)
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
    martial_art_style = models.CharField(max_length=120,null=True,blank=True)
    website = models.CharField(max_length=120,default="",blank=True,null=True)
    modified = models.DateTimeField(auto_now=True, editable=False)
    tags = models.ManyToManyField(Tag)
    city = models.CharField(max_length=2000,null=True, blank=True)
    point = models.PointField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            try:
                geocoder = mapbox.Geocoder(access_token="pk.eyJ1Ijoic2Znb256YWxlejIwNiIsImEiOiJjbGRsNTE5OGswdHh0M3Btc2RuODVmM2F1In0.Xnkdku_W_aclNetMgvK-Og")
                response = geocoder.forward(self.address)
                if response.status_code == 200 and response.geojson()['features']:
                    feature = response.geojson()['features'][0]
                    self.latitude = feature['center'][1]
                    self.longitude = feature['center'][0]
                    self.point = Point(self.latitude, self.longitude)
            except Exception as e:
                print(e)
        super(SchoolGym, self).save(*args, **kwargs)



class Personal(models.Model):
    address = models.CharField(max_length=2000,blank=True,null=True)
    zip_code = models.CharField(max_length=200,blank=True,null=True)
    contact_title = models.CharField(max_length=2000,blank=True,null=True)
    comments_by_data_entry_associate = models.CharField(max_length=2000,blank=True,null=True)
    is_more_information_coming_soon = models.CharField(max_length=2000,blank=True,null=True)
    event_flyer_material = models.CharField(max_length=2000,blank=True,null=True)
    online_registration_link = models.CharField(max_length=2000,default="",blank=True,null=True)
    country = models.CharField(max_length=2000,blank=True,null=True)
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    city = models.CharField(max_length=2000,null=True, blank=True)
    point = models.PointField(null=True, blank=True)
    image = models.ImageField(upload_to='personal_images/', null=True,blank=True) 
    martial_art_style = models.CharField(max_length=120,null=True,blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True, editable=False,null=True,blank=True)
    updated_at =models.DateField(auto_now=True, editable=False,null=True,blank=True)

EVENTS_TYPE = (
    ('Events', 'Events'),
    ('SeminarInformation', 'SeminarInformation'),
    ('SchoolGym', 'SchoolGym'),
    ('Personal', 'Personal'),
)

class all_events_details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    events = models.ForeignKey(Events, on_delete=models.CASCADE,null=True,blank=True)
    seminarnformation = models.ForeignKey(SeminarInformation, on_delete=models.CASCADE,null=True,blank=True)
    schoolgym = models.ForeignKey(SchoolGym, on_delete=models.CASCADE,null=True,blank=True)
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE,null=True,blank=True)
    type = models.CharField(max_length=255,choices=EVENTS_TYPE)
    created_at = models.DateField(auto_now=True, editable=False,null=True,blank=True)
    updated_at =models.DateField(auto_now=True, editable=False,null=True,blank=True) 
    modified = models.DateTimeField(auto_now=True, editable=False)



class Pages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,null=True,blank=True)
    contant = models.TextField()
    created_at = models.DateField(auto_now=True, editable=False,null=True,blank=True)
    updated_at =models.DateField(auto_now=True, editable=False,null=True,blank=True)
    



class PagesImage(models.Model):
    title = models.CharField(max_length=255,null=True,blank=True)
    image = models.ImageField(upload_to='test_images/', null=True,blank=True) 
    

    

class Userbackgroundimage(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    image = models.ImageField(upload_to='Userbackground_images/', null=True,blank=True) 
    




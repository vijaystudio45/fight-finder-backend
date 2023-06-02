from rest_framework import serializers
from .models import User,Add_Blog,Contact,Events,UserContact,SeminarInformation,SchoolGym,all_events_details,Pages,PagesImage,Tag,Userbackgroundimage,Personal
from django.contrib.auth import get_user_model
from geopy.distance import geodesic
from rest_framework_simplejwt.tokens import RefreshToken


class RegistrationSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('role','email','first_name','last_name', 'mobile_number','password','confirm_password')


    def __init__(self, *args, **kwargs):
        super(RegistrationSerializer, self).__init__(*args, **kwargs)
        self.fields['mobile_number'].error_messages['blank'] = 'Mobile Number Required'
        # self.fields['mobile_number'].error_messages['unique'] = 'Mobile Number Already Exist'
        self.fields['password'].error_messages['blank'] = 'Password Required'
        self.fields['confirm_password'].error_messages['blank'] = 'Confirm Password Required'
        self.fields['email'].error_messages['blank'] = 'Email Required'
        # self.fields['email'].error_messages['unique'] = 'Email Already Exist'
       
             

 

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance    
 



class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=200, required=True)
    confirm_password = serializers.CharField(max_length=200, required=True)
    current_password = serializers.CharField(max_length=200, required=True)    
                  
class SendForgotEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=200, required=True)
    confirm_password = serializers.CharField(max_length=200, required=True)

   



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

   



class UpdateUserProfileSerializer(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        user = obj
        token = get_tokens_for_user(user)
        return token

    class Meta:
        model = get_user_model()
        model = User
        fields = '__all__'
        # fields = ['Social_media_links','first_name','last_name','profile_image_update','mobile_number','username','gender','age','weight','competition_level','zip_code','country','about_me','email','created_at','token']    
    

    profile_image_update = serializers.ImageField(required=False)










class AddBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Add_Blog
        fields = '__all__' 
  


class contactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

    def validate(self, data):
        phone = data.get('phone')
        if not phone.isnumeric(): 
            raise serializers.ValidationError("Phone number must be entered in Number ") 
        if len(phone) < 10 or len(phone) > 13:
            raise serializers.ValidationError("Phone number is not valid")
        return data
             
class UserList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserblockUnblock(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_block']

                      
class UserIsApproved(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_block']
         



class UserContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserContact
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(UserContactSerializer, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages['blank'] = 'Name Required'
        self.fields['email'].error_messages['blank'] = 'Email Required'
        self.fields['message'].error_messages['blank'] = 'Message Required'
        self.fields['phone_number'].error_messages['blank'] = 'Phone Number Required'



class EventsSerializers(serializers.ModelSerializer):
    time = serializers.CharField()

    class Meta:
        model = Events
        fields = '__all__'     

   
                      


class SchoolGymSerializers(serializers.ModelSerializer):
    class Meta:
        model = SchoolGym
        fields = '__all__'   
        
           





class PagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pages
        fields = '__all__'          



class UserSerializers(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields = '__all__'  


class SeminarSerializers(serializers.ModelSerializer):
 
    class Meta:
        model = SeminarInformation
        fields = '__all__'  



class PersonalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Personal
        fields = '__all__'



class all_events_detailsSerializers(serializers.ModelSerializer):
    events =EventsSerializers(required=False)
    seminarnformation = SeminarSerializers(required=False)
    schoolgym = SchoolGymSerializers(required=False)
    personal = PersonalSerializer(required=False)
     
    class Meta:
        model = all_events_details
        fields = '__all__'    





   











class Get_details_detailsSerializers(serializers.ModelSerializer):
    user = UserSerializers(required=False)
    events =EventsSerializers(required=False)
    seminarnformation = SeminarSerializers(required=False)
    schoolgym = SchoolGymSerializers(required=False)
     
    class Meta:
        model = all_events_details
        fields = '__all__'  


class upcomingEvents_detailsSerializers(serializers.ModelSerializer):
    events =EventsSerializers(required=False)
    seminarnformation = SeminarSerializers(required=False)
    schoolgym = SchoolGymSerializers(required=False)
    
    class Meta:
        model = all_events_details
        fields = '__all__'         

    def get_image(self,object):
        if object.image is not None:
            return object.image.url
        




class PageImageSerializers(serializers.ModelSerializer):
 
    class Meta:
        model = PagesImage
        fields = '__all__'  
   
    


 

    

class SchoolSerializers(serializers.ModelSerializer):
    class Meta:
        model = SchoolGym
        fields = ['id','latitude','longitude','country','address','title','image']   
        
class SemSerializers(serializers.ModelSerializer):
    class Meta:
        model = SeminarInformation
        fields = ['id','latitude','longitude','country','address','title','image']   
                

class evSerializers(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id','latitude','longitude','country','address','title','image']   
                                



class newformdetails_detailsSerializers(serializers.ModelSerializer):
    events =evSerializers(required=False)
    seminarnformation = SemSerializers(required=False)
    schoolgym = SchoolSerializers(required=False)
     
    class Meta:
        model = all_events_details
        fields = '__all__'                                  



class followerPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'






class PostUserDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'        




class TagSerializers(serializers.ModelSerializer):
 
    class Meta:
        model = Tag
        fields = '__all__'  


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'





class UserbackgroundSerializers(serializers.ModelSerializer):
    class Meta:
        model = Userbackgroundimage
        fields = '__all__' 



class distanceEventsSerializers(serializers.ModelSerializer):
    time = serializers.CharField()
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Events
        fields = ['id','address', 'zip_code', 'contact_title', 'event_link', 'comments_by_data_entry_associate', 'is_more_information_coming_soon', 'event_flyer_material', 'online_registration_link', 'country', 'latitude', 'longitude', 'time', 'contact_first_name', 'contact_last_name', 'contact_phone_number', 'contact_email', 'contact_social_media_links', 'does_this_event_accept_foreign_participants', 'instructions_for_the_event', 'related_associations_or_organizations', 'title', 'image', 'city', 'start_date', 'end_date', 'status', 'modified', 'created_at', 'updated_at', 'is_approved', 'online_only', 'martial_art_style', 'website', 'tags', 'point', 'event_participants', 'distance']



    def get_distance(self, obj):
        current_location = (self.context['lat'], self.context['lng'])
        event_location = (obj.latitude, obj.longitude)
        distance_km = geodesic(current_location, event_location).kilometers
        distance_miles = distance_km * 0.621371  # Convert kilometers to miles
        return distance_miles






class distanceSchoolGymSerializers(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()

    class Meta:
        model = SchoolGym
        fields = ['id','title', 'address', 'latitude', 'longitude', 'zip_code', 'country', 'owner_first_name', 'owner_last_name', 'owner_phone_number', 'owner_email', 'price_min_ranges', 'price_max_ranges', 'days_of_operation', 'hours_of_operation', 'introduction', 'owner_social_media_links', 'special_instructions', 'is_approved', 'created_at', 'updated_at', 'image', 'martial_art_style', 'website', 'modified', 'tags', 'city', 'point']

    def get_distance(self, obj):
        current_location = (self.context['lat'], self.context['lng'])
        event_location = (obj.latitude, obj.longitude)
        distance_km = geodesic(current_location, event_location).kilometers
        distance_miles = distance_km * 0.621371  # Convert kilometers to miles
        return distance_miles



class upcomingDistance_detailsSerializers(serializers.ModelSerializer):
    events =distanceEventsSerializers(required=False)
    schoolgym = distanceSchoolGymSerializers(required=False)
    seminarnformation = SeminarSerializers(required=False)
    
    class Meta:
        model = all_events_details
        fields = '__all__'         

    def get_image(self,object):
        if object.image is not None:
            return object.image.url

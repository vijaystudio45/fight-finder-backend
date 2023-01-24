from rest_framework import serializers
from .models import User,Add_Blog,Contact,Events,UserContact,SeminarInformation,SchoolGym,all_events_details,Pages
from django.contrib.auth import get_user_model
from datetime import datetime
import io


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
       
             

    # def validate(self, data):
    #     mobile_number = data.get('mobile_number')
    #     email = data.get('email')
    #     # if User.objects.filter(email__iexact=email).exists():
    #     #     raise serializers.ValidationError("User Name and email must be unique")
    #     # if User.objects.filter(email__iexact=email).exists():
    #     #     raise serializers.ValidationError("Email already exist")
    #     # if User.objects.filter(mobile_number__iexact=mobile_number).exists():
    #     #     raise serializers.ValidationError("Mobile Number already exist") 
    #     if not mobile_number.isnumeric(): 
    #         raise serializers.ValidationError("Mobile number must be entered in Number ") 
    #     if len(mobile_number) < 10 or len(mobile_number) > 13:
    #         raise serializers.ValidationError("Mobile numbe is not valid")
    #     return data

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

   

class UpdateUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        model = User
        fields = ['first_name','last_name','profile_image_update','mobile_number','username','gender','age','weight','martial_art_style','competition_level','zip_code','country','about_me','email']    



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
            raise serializers.ValidationError("Phone numbe is not valid")
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



class all_events_detailsSerializers(serializers.ModelSerializer):
    events =EventsSerializers(required=False)
    seminarnformation = SeminarSerializers(required=False)
    schoolgym = SchoolGymSerializers(required=False)
     
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
        


class csvData_detailsSerializers(serializers.ModelSerializer):
    events =EventsSerializers(required=False)
    seminarnformation = SeminarSerializers(required=False)
    schoolgym = SchoolGymSerializers(required=False)
    
    class Meta:
        model = all_events_details
        fields = '__all__'           



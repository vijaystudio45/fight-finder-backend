from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import(
RegistrationSerializer,
LoginSerializer,
ChangePasswordSerializer,
SendForgotEmailSerializer,
ResetPasswordSerializer,
UpdateUserProfileSerializer,
AddBlogSerializer,
contactSerializer,
UserList,
UserblockUnblock,
EventsSerializers,
UserContactSerializer,
all_events_detailsSerializers,
upcomingEvents_detailsSerializers,
PagesSerializers,
SchoolGymSerializers,
SeminarSerializers,
Get_details_detailsSerializers,
csvData_detailsSerializers
)
from .models import User,Add_Blog,Contact,Events,all_events_details,Pages,SchoolGym,SeminarInformation,Industry
from rest_framework.generics import GenericAPIView
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework import permissions
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import uuid
from rest_framework import viewsets
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings 
from django.db.models import Q
from sendgrid.helpers.mail import Mail, Email, To, Content
from .helper.helper import StringEncoder
from contract_project.settings import FRONTEND_SITE_URL,BACKEND_SITE_URL
from rest_framework.generics import  RetrieveUpdateAPIView
from rest_framework import generics
import os
from datetime import datetime
import json  
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
import datetime as dt
from django.http import Http404
import datetime
from datetime import datetime
from datetime import datetime, timedelta
import datetime
import io, csv, pandas as pd
from rest_framework.parsers import FileUploadParser
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
#test
class RegistrationView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        try:
            data = request.data
            serializer = RegistrationSerializer(data=data)
            if serializer.is_valid():
                if User.objects.filter(email=data['email']).exists():   
                    context = {
                        'message': 'Email already exists'
                    }
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)

                if User.objects.filter(mobile_number=data['mobile_number']).exists():
                    context = {
                        'message': 'Mobile number already exists'
                    }
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)

                if data['password'] != data['confirm_password']:
                    context = {
                        'message': 'Passwords do not match'
                    }
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)   

                user = User.objects.create(

                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    username=data['username'].replace(" ", ""),
                    email=data['email'],
                    password=data['password'],
                    mobile_number=data['mobile_number'],
                )
                user.set_password(data['password'])
                if not request.data.get('email_verify'):
                    email = serializer.validated_data['email']
                    from_email = settings.EMAIL_HOST_USER
                    to_email = [email]
                    token = str(uuid.uuid4())
                    decodeId = StringEncoder.encode(self, user.id)
                    subject = "User registered"
                    message = "User registered"
                    htmlMessage = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\
                                        <html xmlns="http://www.w3.org/1999/xhtml">\
                                        <head>\
                                            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\
                                            <title>Mongo DB</title>\
                                            <meta name="viewport" content="width=device-width, initial-scale=1.0" /> </head>\
                                        <body style="margin: 0; padding: 0; background: #eee;">\
                                            <div style="background: rgba(36, 114, 252, 0.06) !important;">\
                                            <table style="font: Arial, sans-serif; border-collapse: collapse; width:600px; margin: 0 auto;" width="600" cellpadding="0" cellspacing="0">\
                                                <tbody>\
                                                <tr>\
                                                    <td style="width: 100%; margin: 36px 0 0;">\
                                                    <div style="padding: 34px 44px; border-radius: 8px !important; background: #fff; border: 1px solid #dddddd5e; margin-bottom: 50px; margin-top: 50px;">\
                                                        <div class="email-logo">\
                                                        </div>\
                                                        <a href="#"></a>\
                                                        <div class="welcome-text">\
                                                        <h1 style="font:24px;"> Welcome <span class="welcome-hand">👋</span>\
                                                        </h1>\
                                                        </div>\
                                                        <div class="welcome-paragraph">\
                                                        <div style="padding: 20px 0px; font-size:16px; color: #384860;">Welcome to Translator Service</div>\
                                                        <div style="padding:10px 0px; font-size: 16px; color: #384860;">Please click the link below to verify your account <br />\
                                                        </div>\
                                                        <div style="padding: 20px 0px; font-size: 16px; color: #384860;"> Sincerely, <br />The Translator service Team </div>\
                                                        </div>\
                                                        <div style="padding-top:40px; cursor: pointer !important;" class="confirm-email-button">\
                                                        <a href='+FRONTEND_SITE_URL+'/verify-email/' +decodeId+ ' style="cursor: pointer;">\
                                                            <button style="height: 56px;padding: 15px 44px; background: #2472fc; border-radius: 8px;border-style: none; color: white; font-size: 16px; cursor: pointer !important;">Confirm Email</button>\
                                                        </a>\
                                                        </div>\
                                                        <div style="padding: 50px 0px;" class="email-bottom-para">\
                                                        <div style="padding: 20px 0px; font-size:16px; color: #384860;">This email was sent by  Translator Service. If you&#x27;d rather not receive this kind of email, Don’t want any more emails from  Translator Service? <a href="#">\
                                                            <span style="text-decoration:underline;"></span>\
                                                            </a>\
                                                        </div>\
                                                        <div style="font-size: 16px;color: #384860;"> © 2023  Translator Service</div>\
                                                        </div>\
                                                    </div>\
                                                    </td>\
                                                </tr>\
                                                </tbody>\
                                            </table>\
                                            </div>\
                                        </body>\
                                        </html>'

                    data = send_mail(subject, message, from_email, to_email, html_message=htmlMessage)
                    user.forget_password_token = token
                else:
                    user.email_verified = True
                user.save()
                return Response({'message': 'User Registered Successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'message': f'{e} is required'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(APIView):
    lookup_url_kwarg = "token"
    lookup_url_kwarg2 = "uid"
    def get(self, request, *args, **kwargs):
        token = self.kwargs.get(self.lookup_url_kwarg)
        uid = self.kwargs.get(self.lookup_url_kwarg2)
        encoded_id = int(StringEncoder.decode(self, uid))
        user_data = User.objects.filter(id=encoded_id, email_verified=False)
        print('user_data',user_data)
        if user_data:
            user_data.update(email_verified=True)
            context = {'message': 'Your email have been confirmed', 'status': status.HTTP_200_OK, 'error': False}
            return Response(context, status=status.HTTP_201_CREATED)
        context = {
            'message': "Something went wrong!",
            'error': True
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }





class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if not user:
            user = User.objects.filter(email=email).first()

        if user is None:
            context = {
                'message': 'Please enter valid login details'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        if user.email_verified == False:
            context = {
                'message': 'Please confirm your email to access your account'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
     
        if not user.check_password(password):
            context = {
                'message': 'Please enter valid login details'
            }

            return Response(context, status=status.HTTP_400_BAD_REQUEST)
   

       
        if user.is_block == False:
            context = {
                'message': 'This user is block'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    

        useremail = user.email      

        token = get_tokens_for_user(user)
        response = Response(status=status.HTTP_200_OK)

        # Set Token Cookie
    
            

        response.set_cookie(key='token', value=token, httponly=True)
        cache.set('token', token, 60)
        response.data = {
            'message': "Login Success",
            'token': token['access'],
            'refresh': token['refresh'],
            'id': user.id,
            'role': user.role,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'mobile_number': user.mobile_number,
            'state': user.state,
            'about_me': user.about_me,
            'gender': user.gender,
            'created_at': user.created_at,
            'age': user.age,
            'weight': user.weight,
            'martial_art_style': user.martial_art_style,
            'competition_level': user.competition_level,
            'zip_code': user.zip_code,
            'country': user.country,
            'profile_image_update': "http://122.160.74.251:8014"+user.profile_image_update.url if user.profile_image_update else '',
            
        }
        return response

# @permission_classes([IsAuthenticated])
class PasswordChange(APIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            new_password = data.validated_data.get('new_password', None)
            confirm_password = data.validated_data.get('confirm_password', None)
            current_password = data.validated_data.get('current_password', None)
            user = User.objects.filter(id=request.user.id).first()
            if new_password != confirm_password:
                return Response({'message': 'New Password and Confirm Password do not match'},
                                status=status.HTTP_400_BAD_REQUEST)
            if not user.check_password(current_password):
                context = {
                    'message': 'Please enter valid current_password.'
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            if user:
                return Response({'message': 'Your Password Changed Successfully.'}, status=status.HTTP_200_OK) 
            else:
                return Response({'message': 'There is an error to changing the password'},status=status.HTTP_400_BAD_REQUEST)



class ForgetPassword(APIView):
    serializer_class = SendForgotEmailSerializer
    
    def post(self, request):
        protocol = request.scheme
        domain = FRONTEND_SITE_URL
        # domain = request.get_host()
        email = request.data
        serializer = SendForgotEmailSerializer(data=email)
        if serializer.is_valid(raise_exception=True):
            email = request.data['email']
            user = User.objects.filter(email=email).first()
            if not user:
                user = User.objects.filter(username=email).first()
                return Response({'message': 'Email does not exists in database'}, status=status.HTTP_400_BAD_REQUEST)
            token = str(uuid.uuid4())
            token_expire_time = datetime.datetime.utcnow() + timedelta(minutes=3)
            user.token_expire_time = token_expire_time
            user.forget_password_token = token
            user.save()
            user_id = user.id
            email_from = settings.EMAIL_HOST_USER
            subject = 'Forgot Password Email'
            message = "\n\n\n\nHI " + str(user.username) + " \n\n link to reset password is :" +str(domain) + "/password-reset/" + str(token) + "/" + str(user_id)
            restUrl =  str(domain)+"/reset-password/" + str(token) + "/" + str(user_id)+"/"

            htmlMessage = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\
                        <html xmlns="http://www.w3.org/1999/xhtml">\
                        <head>\
                            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\
                            <title>Mongo DB</title>\
                            <meta name="viewport" content="width=device-width, initial-scale=1.0" /> </head>\
                        <body style="margin: 0; padding: 0; background: #eee;">\
                            <div style="background: rgba(36, 114, 252, 0.06) !important;">\
                            <table style="font: Arial, sans-serif; border-collapse: collapse; width:600px; margin: 0 auto;" width="600" cellpadding="0" cellspacing="0">\
                                <tbody>\
                                <tr>\
                                    <td style="width: 100%; margin: 36px 0 0;">\
                                    <div style="padding: 34px 44px; border-radius: 8px !important; background: #fff; border: 1px solid #dddddd5e; margin-bottom: 50px; margin-top: 50px;">\
                                        <div class="email-logo">\
                                        <img style="width: 165px;" src="https://webimages.mongodb.com/_com_assets/cms/kuzt9r42or1fxvlq2-Meta_Generic.png" />\
                                        </div>\
                                        <a href="#"></a>\
                                        <div class="welcome-text">\
                                        <h1 style="font:24px;"> Welcome <span class="welcome-hand">👋</span>\
                                        </h1>\
                                        </div>\
                                        <div class="welcome-paragraph">\
                                        <div style="padding: 20px 0px; font-size:16px; color: #384860;">Welcome to Fight Finder!</div>\
                                        <div style="padding:10px 0px; font-size: 16px; color: #384860;">Please click the link below to Reset Password. <br />\
                                        </div>\
                                        <div style="padding: 20px 0px; font-size: 16px; color: #384860;"> Sincerely, <br />The Fight Finder Team </div>\
                                        </div>\
                                        <div style="padding-top:40px; cursor: pointer !important;" class="confirm-email-button">\
                                        <a href="'+restUrl+'" style="cursor: pointer;">\
                                            <button style="height: 56px;padding: 15px 44px; background: #2472fc; border-radius: 8px;border-style: none; color: white; font-size: 16px; cursor: pointer !important;">Reset Password</button>\
                                        </a>\
                                        </div>\
                                        <div style="padding: 50px 0px;" class="email-bottom-para">\
                                        <div style="padding: 20px 0px; font-size:16px; color: #384860;">This email was sent by Fight Finder. If you&#x27;d rather not receive this kind of email, Don’t want any more emails from Fight Finder? <a href="#">\
                                            <span style="text-decoration:underline;"></span>\
                                            </a>\
                                        </div>\
                                        <div style="font-size: 16px;color: #384860;"> © 2023 Fight Finder</div>\
                                        </div>\
                                    </div>\
                                    </td>\
                                </tr>\
                                </tbody>\
                            </table>\
                            </div>\
                        </body>\
                        </html>'
            try:
                send_mail(subject,message, email_from,[email], html_message=htmlMessage, fail_silently=False,)
                return Response({'message': 'Email Send successfully, Please check your email'},status=status.HTTP_200_OK)      
            except Exception as e:
                pass
        else:
            return Response({'message': 'There is an error to sending the data'},status=status.HTTP_400_BAD_REQUEST)



class ResetPassword(APIView):
    serializer_class = ResetPasswordSerializer
    lookup_url_kwarg = "token"
    lookup_url_kwarg2 = "uid"

    def get(self, request, *args, **kwargs):
        serializer_class = ResetPasswordSerializer
        token = self.kwargs.get(self.lookup_url_kwarg)
        uid = self.kwargs.get(self.lookup_url_kwarg2)
        user_data = User.objects.filter(id=uid).first()
        if not user_data.forget_password_token:
            return Response({'token_expire': 'Token Expired'}, status=status.HTTP_400_BAD_REQUEST)
        if token != user_data.forget_password_token:
            return Response({'token_expire': 'Token Expired'}, status=status.HTTP_400_BAD_REQUEST)

        token_expire_time = user_data.token_expire_time.replace(tzinfo=None)
        current_expire_time = datetime.datetime.utcnow()
        if current_expire_time > token_expire_time:
            return Response({'token_expire': 'Token Expired'}, status=status.HTTP_400_BAD_REQUEST)

        context = {
            'token_expire_time': token_expire_time
            # 'current_expire_time': current_expire_time
        }
        response = Response(context, status=status.HTTP_200_OK)
        return response

    
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = request.data['password']
        confirm_password = request.data['confirm_password']

        if password != confirm_password:
            return Response({'message': 'Password and Confirm Password do not match'},status=status.HTTP_400_BAD_REQUEST)
        user_id = self.kwargs.get(self.lookup_url_kwarg2)
        user_data = User.objects.get(id=user_id)
        user_data.set_password(password)
        user_data.forget_password_token = None
        user_data.save()
        if user_data != 0:
            return Response({'message': 'Your Password updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'There is an error to updating the data'}, status=status.HTTP_400_BAD_REQUEST)



class UpdateUserProfile(APIView):
    serializer_class = UpdateUserProfileSerializer


    def post(self, request, format=None):
        try:
            # exist then update
            getUser = User.objects.get(id=request.user.id)
            print(request.data)
            serializer = UpdateUserProfileSerializer(getUser, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                token = get_tokens_for_user(getUser)
                Response_data = ( {
                    
                    'first_name': getUser.first_name,
                    'last_name': getUser.last_name,
                    'mobile_number': getUser.mobile_number,
                    'id': getUser.id,
                    'email': getUser.email,
                    'token': token['access'],
                    'refresh': token['refresh'],
                    'about_me': getUser.about_me,
                    'gender': getUser.gender,
                    'role': getUser.role,
                    'username': getUser.username,
                    'age': getUser.age,
                    'weight': getUser.weight,
                    'martial_art_style': getUser.martial_art_style,
                    'competition_level': getUser.competition_level,
                    'zip_code': getUser.zip_code,
                    'country': getUser.country,
                    'profile_image_update': "http://122.160.74.251:8014"+getUser.profile_image_update.url,
                    }
                )
                return Response({'data':Response_data,'message':'Profile Updated  successful'})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:   
                return Response({'message': 'Profile is not updated, Please try again'}, status=status.HTTP_400_BAD_REQUEST)





class AddBlogViewSet(viewsets.ModelViewSet):
    serializer_class = AddBlogSerializer
    queryset = Add_Blog.objects.all().order_by('-modified')
    filter_backends = [DjangoFilterBackend, SearchFilter] 
    filterset_fields = ['status',]
    
             
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        event_obj =  request.data.get('remove_image')
        serializer = self.get_serializer(instance, data=request.data, partial=partial)   
        if serializer.is_valid():
              if event_obj == "true":
                if os.path.isfile(instance.image.path):   
                    os.remove(instance.image.path)
                    instance.image=None
              instance.save()
        self.perform_update(serializer)
        context = {
            'message': 'Blog Updated Succesfully',
            'status': status.HTTP_200_OK,
            'errors': serializer.errors,
            'data': serializer.data,
        }
        return Response(context)



    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        context = {
            'message': 'Blog Deleted Successfully',
            'status': status.HTTP_204_NO_CONTENT,
            'errors': False,
        }
        return Response(context)      
                     






class contactView(APIView):
    serializer_class = contactSerializer

    def get(self, request, format=None):
        contact = Contact.objects.all()
        serializer = contactSerializer(contact, many=True)
        return Response(serializer.data) 


    def post(self, request):
        try:
            contact_user = Contact.objects.all().first()
            data = request.data
            serializer = contactSerializer(data=data)
            if serializer.is_valid(): 
                
                if contact_user:
                    data = Contact.objects.filter(id=contact_user.id).update(
                        email=data['email'],
                        phone = data['phone'],
                        address=data['address']
                    )
                    return Response({'message': 'contact updated successfully'}, status=status.HTTP_200_OK)
                   
                else:
                    data = Contact.objects.create(
                        email=data['email'],
                        phone = data['phone'],
                        address=data['address']
                    
                    )
                    data.save()        
                
                    return Response({'message': 'contact added successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({'message': f'{e} is required'}, status=status.HTTP_400_BAD_REQUEST)  

    
          

class UserListView(APIView):

    def get(self, request, format=None):
        user = User.objects.all().order_by('-id')
        serializer = UserList(user, many=True)
        return Response(serializer.data)




class UserBlocUnblockkView(APIView):
    serializer_class=UserblockUnblock
    
    def post(self, request, pk,format=None):
        serializer = UserblockUnblock(data=request.data)
        if serializer.is_valid():
            data1 = serializer.validated_data['is_block']
            print(data1)
            data = User.objects.filter(id=pk).update(is_block=serializer.data['is_block'])
            print(data)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserContactView(APIView):
    serializer_class = UserContactSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serailizer = UserContactSerializer(data=data)
            admin_email = Contact.objects.all().first()
            if serailizer.is_valid():
                serailizer.save()
                # data = serailizer_class.validated_data
                name = data.get('name')
                email = data.get('email')
                message = data.get('message')
                phone_number = data.get('phone_number')
                # recipient_list = ['davinder.studio45@gmail.com']
                recipient_list = [admin_email.email]
                email_from = email
                messages =f'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\
                <html xmlns="http://www.w3.org/1999/xhtml">\
                    <head>\
                    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\
                    <title>Fight Finder</title>\
                    <meta name="viewport" content="width=device-width, initial-scale=1.0" /> </head>\
                    <body style="margin: 0; padding: 0; background: #eee;">\
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">\
                        <tr>\
                            <td style="padding: 10px 0 30px 0;">\
                                <table align="center" border="0" cellpadding="0" cellspacing="0" width="700" style="border: 1px solid #cccccc; border-collapse: collapse;">\
                                    <tr>\
                                        <td align="center" bgcolor="#ccc" style="padding: 20px 0 30px 0; color: #153643; font-size: 28px; font-weight: bold; font-family: Arial, sans-serif;"> \
                                            <table width="100%">\
                                                <tr>\
                                                    <td width="50%" style="padding-left:40px;">\
                                                        <img src="http://122.160.74.251:3004/image%205.png" alt="Fight Finder" width="100" height="70" style="display: block;" />\
                                                    </td>\
                                                    <td align="right" style="padding-right:40px;">\
                                                        <small style="font-size:12px; background: #08c; color:#FFF; padding:10px; border-radius: 5px;"><a href="http://www.Fight Finder.com" target="_blank" style="color:#FFF; text-decoration: none;">Shop at Fight Finder</a></small>\
                                                    </td>\
                                                </tr>\
                                            </table>\
                                        </td>\
                                    </tr>\
                                    <tr>\
                                        <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">\
                                            <center style="font-family:Arial; font-size:24px;">\
                                                <h3>Contact Us</h3>\
                                            </center>\
                                            <table border="0" cellpadding="0" cellspacing="0" width="100%">\
                                                <tr>\
                                                    <td style="color: #153643; font-family: Arial, sans-serif; font-size: 16	px;"> <b>Hi Admin</b> </td>\
                                                </tr>\
                                                <tr>\
                                                    <td style="padding: 20px 0 30px 0; color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 20px;">\
                                                        Someone has filled a contact us form, details are mentioned below:<br /><br />\
                                                        <table width="100%" style="line-height:40px;">\
                                                            <tr>\
                                                                <td width="30%">Name:</td>\
                                                                <td>' + name + '</td>\
                                                            </tr>\
                                                            <tr>\
                                                                <td>Email:</td>\
                                                                <td>' +  email + '</td>\
                                                            </tr>\
                                                            <tr>\
                                                                <td>Phone No:</td>\
                                                                <td>' + phone_number + '</td>\
                                                            </tr>\
                                                            <tr>\
                                                                <td>Message:</td>\
                                                                <td>' + message + '</td>\
                                                            </tr>\
                                                        </table>\
                                                        <br /><br /><br />\
                                                        Regards,<br />\
                                                        <b>Fight Finder</b>\
                                                    </td>\
                                                </tr>\
                                            </table>\
                                        </td>\
                                    </tr>\
                                    <tr>\
                                        <td bgcolor="#08c" style="padding: 20px 30px 20px 30px;">\
                                            <table border="0" cellpadding="0" cellspacing="0" width="100%">\
                                                <tr>\
                                                    <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;" width="75%"> &copy; Copyright, All Right Reserved | <a href="http://Fight Finder.com" style="color: #ffffff; font-weight: bold; text-decoration: none;">Fight Finder</a> </td>\
                                                </tr>\
                                            </table>\
                                        </td>\
                                    </tr>\
                                </table>\
                            </td>\
                        </tr>\
                    </table>\
                    </body>\
                    </html>'
                subject = 'Contact Form'
                try:
                    send_mail(subject, message, email_from, recipient_list, html_message=messages, fail_silently=False,)
                
                    return Response({"success": "Message Sent Successfully"}, status=status.HTTP_200_OK)
                except Exception as e:
                    pass  
            else:
                return Response({'message': serailizer.errors}, status=status.HTTP_400_BAD_REQUEST)    
        except KeyError as e:
            return Response({'message': f'{e} is required'}, status=status.HTTP_400_BAD_REQUEST)
        





class UpcomingEventsViewDetail(APIView):
    serializer_class = upcomingEvents_detailsSerializers

    def get_object(self, pk):
        # Returns an object instance that should 
        # be used for detail views.
        try:
            return all_events_details.objects.get(pk=pk)
        except all_events_details.DoesNotExist:
            raise Http404
   
    def get(self, request, pk, format=None):
        transformer = self.get_object(pk)
        serializer = upcomingEvents_detailsSerializers(transformer)
        return Response(serializer.data)



    
 






class pagesViewSet(viewsets.ModelViewSet): 
    serializer_class = PagesSerializers
    queryset = Pages.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter] 
    filterset_fields = ['title']
     

    def create(self, request, *args, **kwargs):
        get_pages = request.data.get('contant')
        get_title = request.data.get('title')
        user_id =  request.data.get('user')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if Pages.objects.filter(title=get_title).exists():
                Pages.objects.filter(title=get_title).update(contant=get_pages,title=get_title,user=user_id)
                return Response({'message': 'Pages updated successfully'}, status=status.HTTP_200_OK)  
            else:
                self.perform_create(serializer)
                return Response({'message': 'Pages added successfully'}, status=status.HTTP_200_OK)  
            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        context = {
            'message': 'Pages Deleted Successfully',
            'status': status.HTTP_204_NO_CONTENT,
            'errors': False,
        }
        return Response(context)  







def str_to_time(value):
    data= datetime.strptime(value.replace("T"," ").replace("Z",""), '%Y-%m-%d %H:%M:%S.%f')
    return data.strftime("%H:%M:%S")



class AllEventViewSet(viewsets.ModelViewSet):
    serializer_class = EventsSerializers
    serializer_class1 = all_events_detailsSerializers
    queryset = Events.objects.all() 
   

    def create(self, request, *args, **kwargs):
        event_obj =  request.data.getlist('event')
        image_obj =  request.FILES.getlist('image')
        for index,i in enumerate(event_obj):
            data = json.loads(i)
            serializer = self.serializer_class(data=data)
            serializer1 = self.serializer_class1(data=data)
            if serializer.is_valid() and serializer1.is_valid():
                data = serializer.save(time = str_to_time(data.get('time')),image=image_obj[index])
                serializer1.save(events=data) 
            else:
              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
        return Response({'data':serializer.data,'message':'Events added successful'})


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({'data':serializer.data,'message':'Events updated successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        context = {
            'message': 'event Deleted Successfully',
            'status': status.HTTP_204_NO_CONTENT,
            'errors': False,
        }
        return Response(context)      
                                 
           






class SchoolGymViewSet(viewsets.ModelViewSet):
    serializer_class = SchoolGymSerializers
    serializer_class1 = all_events_detailsSerializers
    queryset = SchoolGym.objects.all() 
   

    def create(self, request, *args, **kwargs):
        school_obj =  request.data.getlist('school')
        image_obj =  request.FILES.getlist('image')
        for index,i in enumerate(school_obj):
            data = json.loads(i)
            serializer = self.serializer_class(data=data)
            serializer1 = self.serializer_class1(data=data)
            if serializer.is_valid() and serializer1.is_valid():
                data = serializer.save(image=image_obj[index]) 
                serializer1.save(schoolgym=data) 
            else:
              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       
        return Response({'data':serializer.data,'message':'School added successful'})    


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({'data':serializer.data,'message':'School updated successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

       

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        context = {
            'message': 'school Deleted Successfully',
            'status': status.HTTP_204_NO_CONTENT,
            'errors': False,
        }
        return Response(context)      
                             
    





class SeminarViewSet(viewsets.ModelViewSet):
    serializer_class = SeminarSerializers
    serializer_class1 = all_events_detailsSerializers
    queryset = SeminarInformation.objects.all() 
   

    def create(self, request, *args, **kwargs):
        seminar_obj =  request.data.getlist('seminar')
        image_obj =  request.FILES.getlist('image')
        for index,i in enumerate(seminar_obj):
            data = json.loads(i)
            serializer = self.serializer_class(data=data)
            serializer1 = self.serializer_class1(data=data)
            if serializer.is_valid() and serializer1.is_valid():
                data = serializer.save(image=image_obj[index]) 
                serializer1.save(seminarnformation=data) 
            else:
              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       
        return Response({'data':serializer.data,'message':'Seminar added successful'})


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({'data':serializer.data,'message':'Seminar Updated successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        context = {
            'message': 'seminar Deleted Successfully',
            'status': status.HTTP_204_NO_CONTENT,
            'errors': False,
        }
        return Response(context)      
                        
        
            


class allModelDataViewSet(viewsets.ModelViewSet):
    serializer_class = all_events_detailsSerializers
    queryset = all_events_details.objects.all().order_by('-id') 






class OnlyUserDataView(viewsets.ModelViewSet):
    serializer_class = Get_details_detailsSerializers
    queryset = all_events_details.objects.all()


    def list(self, request):
        print(request.user.id)
        data = all_events_details.objects.filter(Q (user=request.user.id)& Q(user__role = 1))
        serializer = Get_details_detailsSerializers(data, many=True)
        return Response(serializer.data) 
 



class UpcomingEventsView(viewsets.ModelViewSet):
    serializer_class = upcomingEvents_detailsSerializers
    queryset = all_events_details.objects.all().order_by('-id') 
    filter_backends = [SearchFilter]
    search_fields = ['events__title','seminarnformation__title','schoolgym__title']
    
  
    def list(self, request, format=None):
        upcoming_events =  self.filter_queryset(self.get_queryset()).filter(Q (events__end_date__gte=dt.datetime.today())& Q (events__is_approved = True)|Q (seminarnformation__end_date__gte=dt.datetime.today())& Q (seminarnformation__is_approved = True)|Q(schoolgym__created_at__lte=dt.datetime.today())& Q (schoolgym__is_approved = True))
        serializer = upcomingEvents_detailsSerializers(upcoming_events, many=True,context={'request':request})
        return Response(serializer.data) 




class PastEventsView(viewsets.ModelViewSet):
    serializer_class = upcomingEvents_detailsSerializers
    queryset = all_events_details.objects.all().order_by('-id') 
    filter_backends = [SearchFilter]
    search_fields = ['events__title','seminarnformation__title','schoolgym__title']


    def list(self, request, format=None):
        past_events = self.filter_queryset(self.get_queryset()).filter(Q (events__start_date__lte=dt.datetime.today())& Q (events__is_approved = True)|Q (seminarnformation__start_date__lte=dt.datetime.today())& Q (seminarnformation__is_approved = True))
        serializer = upcomingEvents_detailsSerializers(past_events, many=True,context={'request':request})
        return Response(serializer.data)



from django.core.files import File
from urllib.request import urlopen
class UploadCsvFileView(generics.CreateAPIView):
    # serializer_class = SchoolGymSerializers
    
    def post(self, request, *args, **kwargs):
        serializer = EventsSerializers
        serializer1 = SeminarSerializers
        serializer2 = SchoolGymSerializers
        image_url = 'http://122.160.74.251:3004/image%205.png'
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        file = request.FILES['file']
        type1 =  request.data.getlist('type')
        user_obj =  request.data.getlist('user')
        print("---=-=-=-=",user_obj)
        reader = pd.read_csv(file)
        for _, row in reader.iterrows():
            if 'Events' in type1:
                new_file = serializer(data=
                    {"address": row['address'],
                     "zip_code": row['zip_code'], 
                     "country": row['country'],                              
                     "organizer_first_name": row['organizer_first_name'],
                     "organizer_last_name": row['organizer_last_name'],
                     "organizer_phone_number": row['organizer_phone_number'], 
                     "organizer_email": row['organizer_email'],                  
                     "organizer_social_media_links": row['organizer_social_media_links'],                 
                     "does_this_event_accept_foreign_participants": row['does_this_event_accept_foreign_participants'],      
                     "instructions_for_the_event": row['instructions_for_the_event'],  
                     "related_associations_or_organizations": row ['related_associations_or_organizations'],                                
                     "title": row['title'],
                     "time": row['time'],                
                    #  "image": row['image'],
                     "description": row['description'], 
                     "start_date": row["start_date"],
                     "end_date" : row['end_date'], 
                     "status": row["status"],                                     
                     "organizer_social_media_links": row['organizer_social_media_links'],
                     "created_at": row['created_at'], 
                     "updated_at": row['updated_at'],   
                     "is_approved": row['is_approved'], 
                     "modified": row['modified'],                                                        
                                     
                    }) 
                if new_file.is_valid():         
                    events_obj = new_file.save()
                    save_image_from_url(events_obj,image_url)
                    data =all_events_details.objects.create(user_id=1,events=events_obj,type=type1)
                    data.save() 
                else:
                    return Response(new_file.errors, status=400) 
               
            if 'SeminarInformation' in type1:
                new_file = serializer1(data=
                    {"address": row['address'],
                     "zip_code": row['zip_code'], 
                     "country": row['country'],                              
                     "organizer_first_name": row['organizer_first_name'],
                     "organizer_last_name": row['organizer_last_name'],
                     "organizer_phone_number": row['organizer_phone_number'], 
                     "organizer_email": row['organizer_email'],   
                     "organizer_social_media_links": row['organizer_social_media_links'], 
                     "does_this_event_accept_foreign_participants": row['does_this_event_accept_foreign_participants'],  
                     "why_is_this_seminar_only_open_to_this_group_of_people": row['why_is_this_seminar_only_open_to_this_group_of_people'],  
                     "cost_of_seminar": row['cost_of_seminar'],  
                     "title": row['title'],   
                    #  "image": row['image'],
                     "special_instructions": row['special_instructions'], 
                     "details": row['details'],
                     "start_date": row["start_date"],
                     "end_date" : row['end_date'],                   
                     "created_at": row['created_at'], 
                     "updated_at": row['updated_at'],   
                     "is_approved": row['is_approved'],                                      
                                                        
                     })
                if new_file.is_valid():         
                    seminar_data = new_file.save()
                    save_image_from_url(seminar_data,image_url)
                    data =all_events_details.objects.create(user_id=1,seminarnformation=seminar_data,type=type1)
                    data.save()
                    # return Response({"status":"Data saved successfully"} ,status=status.HTTP_201_CREATED)  
                else:
                    return Response(new_file.errors, status=400)

            if 'SchoolGym' in type1:
                new_file = serializer2(data=
                    {"address": row['address'],
                     "zip_code": row['zip_code'], 
                     "country": row['country'],                              
                     "owner_first_name": row['owner_first_name'],
                     "owner_last_name": row['owner_last_name'],
                     "owner_phone_number": row['owner_phone_number'], 
                     "owner_email": row['owner_email'],   
                     "price_min_ranges": row['price_min_ranges'], 
                     "price_max_ranges": row['price_max_ranges'],  
                     "days_of_operation": row['days_of_operation'],  
                     "hours_of_operation": row['hours_of_operation'],  
                     "title": row['title'],   
                    #  "image": row['image'],
                     "special_instructions": row['special_instructions'], 
                     "introduction": row['introduction'],   
                     "owner_social_media_links": row['owner_social_media_links'],
                     "created_at": row['created_at'], 
                     "updated_at": row['updated_at'],   
                     "is_approved": row['is_approved'],                                      
                                                        
                     })
                if new_file.is_valid():      
                    new_data=new_file.save()
                    save_image_from_url(new_data,image_url)
                    data =all_events_details.objects.create(user_id=1,schoolgym=new_data,type=type1)
                    data.save() 
                else:
                    return Response(new_file.errors, status=400)

        return Response({"status":"Data saved successfully"} ,status=status.HTTP_201_CREATED)  

        # return Response({"status": ""},status.HTTP_201_CREATED)






def save_image_from_url(model, url):
    r = requests.get(url)

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(r.content)
    img_temp.flush()

    model.image.save("image.jpg", File(img_temp), save=True)

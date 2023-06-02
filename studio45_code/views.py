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
PageImageSerializers,
newformdetails_detailsSerializers,
TagSerializers,
UserbackgroundSerializers,
upcomingDistance_detailsSerializers,
UserSerializers

)
from .models import User,Add_Blog,Contact,Events,all_events_details,Pages,SchoolGym,SeminarInformation,PagesImage,Tag,Userbackgroundimage,Personal
from rest_framework.generics import GenericAPIView
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
import uuid
from rest_framework import viewsets
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings 
from django.db.models import Q
from .helper.helper import StringEncoder
from contract_project.settings import FRONTEND_SITE_URL,BACKEND_SITE_URL
import os
import json  
from rest_framework.filters import SearchFilter,OrderingFilter
import datetime as dt
from django.http import Http404
import datetime
from datetime import datetime
import io, csv, pandas as pd
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime, timedelta
from rest_framework.generics import UpdateAPIView
import random
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import GeometryDistance
from django.contrib.gis.measure import Distance
import pytz
import urllib.request
from rest_framework import generics








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
                                                        <div style="padding: 20px 0px; font-size:16px; color: #384860;">Welcome to Martial Nexus !</div>\
                                                        <div style="padding:10px 0px; font-size: 16px; color: #384860;">Please click the button below to verify your account <br />\
                                                        </div>\
                                                        <div style="padding: 20px 0px; font-size: 16px; color: #384860;"> Sincerely, <br />The Martial Nexus ! Team </div>\
                                                        </div>\
                                                        <div style="padding-top:40px; cursor: pointer !important;" class="confirm-email-button">\
                                                        <a href='+FRONTEND_SITE_URL+'/verify-email/' +decodeId+ ' style="cursor: pointer;">\
                                                            <button style="height: 56px;padding: 15px 44px; background: #2472fc; border-radius: 8px;border-style: none; color: white; font-size: 16px; cursor: pointer !important;">Confirm Email</button>\
                                                        </a>\
                                                        </div>\
                                                        <div style="padding: 50px 0px;" class="email-bottom-para">\
                                                        <div style="padding: 20px 0px; font-size:16px; color: #384860;">This email was sent by  Martial Nexus !. If you&#x27;d rather not receive this kind of email, Don’t want any more emails from  Martial Nexus ? <a href="#">\
                                                            <span style="text-decoration:underline;"></span>\
                                                            </a>\
                                                        </div>\
                                                        <div style="font-size: 16px;color: #384860;"> © 2023  Martial Nexus !</div>\
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
        if user_data:
            user_data.update(email_verified=True)
            context = {'message': 'Your email have been confirmed', 'status': status.HTTP_200_OK, 'error': False}
            return Response(context, status=status.HTTP_201_CREATED)
        else:
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
            'Social_media_links': user.Social_media_links,
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
            'competition_level': user.competition_level,
            'zip_code': user.zip_code,
            'country': user.country,
            'profile_image_update': "http://43.205.65.56:8000"+user.profile_image_update.url if user.profile_image_update else '',
            
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
            if  user and not user.email_verified:
                return Response({'message': 'Please confirm your email to access your account'}, status=status.HTTP_400_BAD_REQUEST)
            token = str(uuid.uuid4())
            token_expire_time = datetime.utcnow() + timedelta(minutes=3)
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
                                        <img style="width: 165px;" src="http://122.160.74.251:3004/MN big.png" />\
                                        </div>\
                                        <a href="#"></a>\
                                        <div class="welcome-text">\
                                        <h1 style="font:24px;"> Welcome <span class="welcome-hand">👋</span>\
                                        </h1>\
                                        </div>\
                                        <div class="welcome-paragraph">\
                                        <div style="padding: 20px 0px; font-size:16px; color: #384860;">Welcome to Martial Nexus !</div>\
                                        <div style="padding:10px 0px; font-size: 16px; color: #384860;">Please click the button below to Reset Password. <br />\
                                        </div>\
                                        <div style="padding: 20px 0px; font-size: 16px; color: #384860;"> Sincerely, <br />The Martial Nexus  Team </div>\
                                        </div>\
                                        <div style="padding-top:40px; cursor: pointer !important;" class="confirm-email-button">\
                                        <a href="'+restUrl+'" style="cursor: pointer;">\
                                            <button style="height: 56px;padding: 15px 44px; background: #2472fc; border-radius: 8px;border-style: none; color: white; font-size: 16px; cursor: pointer !important;">Reset Password</button>\
                                        </a>\
                                        </div>\
                                        <div style="padding: 50px 0px;" class="email-bottom-para">\
                                        <div style="padding: 20px 0px; font-size:16px; color: #384860;">This email was sent by Martial Nexus . If you&#x27;d rather not receive this kind of email, Don’t want any more emails from Martial Nexus ? <a href="#">\
                                            <span style="text-decoration:underline;"></span>\
                                            </a>\
                                        </div>\
                                        <div style="font-size: 16px;color: #384860;"> © 2023 Martial Nexus </div>\
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
                return Response({'message': 'Email Send Successfully, Please check your email'},status=status.HTTP_200_OK)      
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
            return Response({'message': 'Your Password updated Successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'There is an error to updating the data'}, status=status.HTTP_400_BAD_REQUEST)






class UpdateUserProfile(UpdateAPIView):
    serializer_class = UpdateUserProfileSerializer
    queryset = User.objects.all()


    def get_object(self):
        return self.request.user
        
    

    def perform_update(self, serializer):
        getUser = User.objects.get(id=self.request.user.id)
        profile_image = self.request.data.get('profile_image_update', None)
        if profile_image is not None:
            serializer.validated_data['profile_image_update'] = profile_image
        serializer.save()
        token = get_tokens_for_user(getUser)
        data = {
            'user': serializer.data,
            'token': token
        }
        return Response(data, status=status.HTTP_200_OK)
        # return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)






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
            'message': 'Blog Updated Successfully',
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
                    return Response({'message': 'contact updated Successfully'}, status=status.HTTP_200_OK)
                   
                else:
                    data = Contact.objects.create(
                        email=data['email'],
                        phone = data['phone'],
                        address=data['address']
                    
                    )
                    data.save()        
                
                    return Response({'message': 'contact added Successfully'}, status=status.HTTP_200_OK)
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
            data = User.objects.filter(id=pk).update(is_block=serializer.data['is_block'])  
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
                                                        <img src="http://122.160.74.251:3004/MN.png" alt="Martial Nexus " width="100" height="70" style="display: block;" />\
                                                    </td>\
                                                    <td align="right" style="padding-right:40px;">\
                                                        <small style="font-size:12px; background: #08c; color:#FFF; padding:10px; border-radius: 5px;"><a href="http://www.Martial Nexus .com" target="_blank" style="color:#FFF; text-decoration: none;">Shop at Martial Nexus </a></small>\
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
                                                        <b>Martial Nexus </b>\
                                                    </td>\
                                                </tr>\
                                            </table>\
                                        </td>\
                                    </tr>\
                                    <tr>\
                                        <td bgcolor="#08c" style="padding: 20px 30px 20px 30px;">\
                                            <table border="0" cellpadding="0" cellspacing="0" width="100%">\
                                                <tr>\
                                                    <td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;" width="75%"> &copy; Copyright, All Right Reserved | <a href="http://Martial Nexus .com" style="color: #ffffff; font-weight: bold; text-decoration: none;">Martial Nexus </a> </td>\
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
                return Response({'message': 'Pages updated Successfully'}, status=status.HTTP_200_OK)  
            else:
                self.perform_create(serializer)
                return Response({'message': 'Pages added Successfully'}, status=status.HTTP_200_OK)  
            
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







# def str_to_time(value):
#     data= datetime.strptime(value.replace("T"," ").replace("Z",""), '%Y-%m-%d %H:%M:%S.%f')
#     return data.strftime("%H:%M:%S")



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
                if image_obj and image_obj[index]:
                    data = serializer.save(image=image_obj[index])
                else:
                   data = serializer.save(image=None)
                serializer1.save(events=data) 
            else:
              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
        return Response({'data':serializer.data,'message':'Events added Successfully'})


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({'data':serializer.data,'message':'Events updated Successfully'})
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
                if image_obj and image_obj[index]:
                    data = serializer.save(image=image_obj[index]) 
                else:
                    data = serializer.save(image=None) 
                serializer1.save(schoolgym=data) 
            else:
              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       
        return Response({'data':serializer.data,'message':'School added Successfully'})    


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({'data':serializer.data,'message':'School updated Successfully'})
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
                if image_obj and  image_obj[index]:
                    data = serializer.save(image=image_obj[index]) 
                else:
                    data = serializer.save(image=None) 
                serializer1.save(seminarnformation=data) 
            else:
              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       
        return Response({'data':serializer.data,'message':'Seminar added Successfully'})


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({'data':serializer.data,'message':'Seminar Updated Successfully'})
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
                        
        

class PersonalViewSet(viewsets.ModelViewSet):
    queryset = Personal.objects.all()
    serializer_class1 = all_events_detailsSerializers
    queryset = SeminarInformation.objects.all() 


    def create(self, request, *args, **kwargs):
        seminar_obj = request.data.get('Personal')
        image_obj = request.FILES.get('image')

        data = json.loads(seminar_obj)
        serializer = self.serializer_class(data=data)
        serializer1 = self.serializer_class1(data=data)

        if serializer.is_valid() and serializer1.is_valid():
            if image_obj:
                data = serializer.save(image=image_obj)  # Save the image_obj directly
            else:
                data = serializer.save(image=None)

            serializer1.save(seminarnformation=data)
            return Response({'data': serializer.data, 'message': 'Personal added Successfully'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     
        

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({'data':serializer.data,'message':'Personal Updated Successfully'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        context = {
            'message': 'Personal Deleted Successfully',
            'status': status.HTTP_204_NO_CONTENT,
            'errors': False,
        }
        return Response(context)
            



            


class allModelDataViewSet(viewsets.ModelViewSet):
    serializer_class = Get_details_detailsSerializers
    queryset = all_events_details.objects.all().order_by('-id') 

    def list(self, request):
        data = all_events_details.objects.all().order_by('-id') 
        serializer = Get_details_detailsSerializers(data, many=True,context={'request':request})
        return Response(serializer.data)



class IsApprovedDataViewSet(viewsets.ModelViewSet):
    serializer_class = all_events_detailsSerializers
    queryset = all_events_details.objects.all().order_by('-id') 


    def list(self, request):
        data = all_events_details.objects.filter(Q (seminarnformation__is_approved = True)| Q (events__is_approved = True) |Q (schoolgym__is_approved = True))
        serializer = Get_details_detailsSerializers(data, many=True,context={'request':request})
        return Response(serializer.data)
    




class OnlyUserDataView(viewsets.ModelViewSet):
    serializer_class = Get_details_detailsSerializers
    queryset = all_events_details.objects.all()


    def list(self, request):
        data = all_events_details.objects.filter(Q (user=request.user.id)& Q(user__role = 1))
        serializer = Get_details_detailsSerializers(data, many=True,context={'request':request})
        return Response(serializer.data) 
 





class allEventsDataListAPIView(generics.ListAPIView):
    serializer_class = upcomingDistance_detailsSerializers
    queryset = all_events_details.objects.all().select_related('events', 'seminarnformation', 'schoolgym').prefetch_related('events__tags', 'seminarnformation__tags', 'schoolgym__tags').order_by('-created_at')
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    distance_filter_field = 'events__point'
    ordering_fields = ['created_at']
    ordering = ['created_at']
    filterset_fields = ['type']
    search_fields = [
        'events__title', 'events__address', 'events__country',
        'seminarnformation__title', 'seminarnformation__address', 'seminarnformation__country',
        'schoolgym__title', 'events__martial_art_style', 'seminarnformation__martial_art_style',
        'schoolgym__martial_art_style', 'schoolgym__address', 'events__tags__tag_name',
        'schoolgym__country', 'seminarnformation__tags__tag_name', 'schoolgym__tags__tag_name',
    ]

    def list(self, request, format=None):
        judo = request.GET.get('Judo', None)
        online_only = request.GET.get('online_only', None)
        q_judo = Q()
        if judo:
            q_judo = Q(
                events__martial_art_style=judo,
                seminarnformation__martial_art_style=judo,
                schoolgym__martial_art_style=judo
            )
        q_online_only = Q()
        if online_only:
            q_online_only = Q(
                events__online_only=online_only,
                seminarnformation__online_only=online_only,
                schoolgym__online_only=online_only
            )
        
        today = dt.datetime.today()
        upcoming_events = self.filter_queryset(self.get_queryset()).filter(
            (
                Q(events__start_date__gt=today, events__is_approved=True) |
                Q(seminarnformation__start_date__gt=today, seminarnformation__is_approved=True) |
                Q(schoolgym__created_at__lte=today, schoolgym__is_approved=True)
            ) & q_judo & q_online_only
        )
        
        lat_obj = float(request.GET.get("lat"))
        lng_obj = float(request.GET.get("lng"))

        serializer = self.get_serializer(upcoming_events, many=True, context={'request': request, 'lat': lat_obj, 'lng': lng_obj})
        return Response(serializer.data)


class events_map_location(viewsets.ModelViewSet):
    serializer_class = newformdetails_detailsSerializers
    queryset = all_events_details.objects.all().order_by('-created_at')

    # serializer_class = upcomingEvents_detailsSerializers
    # queryset = all_events_details.objects.all().order_by('-id') 
    filter_backends = [SearchFilter,OrderingFilter,DjangoFilterBackend]
    distance_filter_field = 'events__point'
    ordering_fields = ['created_at']
    ordering = ['created_at']
    filterset_fields = ['type']
    search_fields = ['events__title','seminarnformation__title','schoolgym__title','events__martial_art_style','seminarnformation__martial_art_style','schoolgym__martial_art_style','events__tags__tag_name','seminarnformation__tags__tag_name','schoolgym__tags__tag_name']

    def get_queryset(self):
        today = dt.datetime.today()
        queryset = all_events_details.objects.filter(
            Q(events__end_date__gte=today) & Q(events__is_approved=True) |
            Q(seminarnformation__end_date__gte=today) & Q(seminarnformation__is_approved=True)
        )
        return queryset

    def list(self, request, format=None):

        try:
            lat_obj = float(request.GET.get("lat"))  
            lng_obj = float(request.GET.get("lng"))  
            distance_obj = float(request.GET.get("distance"))
            unit = request.GET.get("distance_type")  # default to kilometers if not provided
        except ValueError:
            return Response({'error': 'Invalid query parameters'}, status=status.HTTP_400_BAD_REQUEST)

        if not distance_obj:
            distance_obj = None  # set default distance to 1000 kilometers (i.e. very large value)

        try:
            distance = float(distance_obj)
        except ValueError:
            return Response({'error': 'Invalid query parameters'}, status=status.HTTP_400_BAD_REQUEST)

        target_point = Point(lat_obj, lng_obj)

        if unit == "km":
            distance = Distance(km=distance_obj)
        elif unit == "mi":
            distance = Distance(mi=distance_obj)
        else:
            return Response({'error': 'Invalid unit of measurement'}, status=status.HTTP_400_BAD_REQUEST)

        # Search for events within the given distance
        if distance_obj:
            upcoming_events = self.filter_queryset(self.get_queryset()).filter(
                Q(events__point__distance_lte=(target_point, distance)) |
                Q(seminarnformation__point__distance_lte=(target_point, distance)) |
                Q(schoolgym__point__distance_lte=(target_point, distance))
            ).filter(
                (Q(events__start_date__gt=dt.datetime.today()) & Q(events__is_approved=True)) |
                (Q(seminarnformation__start_date__gt=dt.datetime.today()) & Q(seminarnformation__is_approved=True)) |
                (Q(schoolgym__created_at__lte=dt.datetime.today()) & Q(schoolgym__is_approved=True))
            )
        if not upcoming_events or not distance_obj:
            target_point = Point(lat_obj, lng_obj,srid=4326)
            upcoming_events = self.filter_queryset(self.get_queryset()).annotate(distance=GeometryDistance("events__point", target_point)).order_by("distance")[:5]
        serializer = upcomingEvents_detailsSerializers(upcoming_events, many=True, context={'request':request})
        return Response(serializer.data)




class UpcomingEventsView(viewsets.ModelViewSet):
    serializer_class = upcomingEvents_detailsSerializers
    queryset = all_events_details.objects.all().order_by('-id') 
    filter_backends = [SearchFilter,OrderingFilter,DjangoFilterBackend]
    distance_filter_field = 'events__point'
    ordering_fields = ['created_at']
    ordering = ['created_at']
    filterset_fields = ['type']
    search_fields = ['events__title','events__address','events__country','seminarnformation__title','seminarnformation__country','seminarnformation__address','schoolgym__title','schoolgym__address','schoolgym__country','events__martial_art_style','seminarnformation__martial_art_style','schoolgym__martial_art_style','events__tags__tag_name','seminarnformation__tags__tag_name','schoolgym__tags__tag_name']

    def get_queryset(self):
        today = dt.datetime.today()
        queryset = all_events_details.objects.select_related('events', 'seminarnformation', 'schoolgym').filter(
            Q(events__end_date__gte=today, events__is_approved=True) |
            Q(seminarnformation__end_date__gte=today, seminarnformation__is_approved=True)
        )
        return queryset

    
    def list(self, request, format=None):   
        
        lat_obj = float(request.GET.get("lat",None)) 
        lng_obj = float(request.GET.get("lng",None)) 
        distance_obj = request.GET.get("distance",None)
        unit = request.GET.get("distance_type",None)  
        Judo = request.GET.get('Judo', None)
        online_only = request.GET.get('online_only', None)
        q_Judo = Q()
        if Judo:
            q_Judo = Q(Q(Q(events__martial_art_style=Judo) | Q(seminarnformation__martial_art_style=Judo)| Q(schoolgym__martial_art_style=Judo)))
        q_online_only = Q()
        if online_only:
            q_online_only = Q(Q(Q(events__online_only=online_only)  | Q (seminarnformation__online_only=online_only) | Q (seminarnformation__online_only=online_only) | Q (seminarnformation__online_only=online_only) ))
        if unit == "km":
            if distance_obj:
                distance = Distance(km=(distance_obj))
            else:
                distance= None
        elif unit == "mi":
            if distance_obj:
                distance = Distance(mi=(distance_obj))
            else:
                distance=None
        else:
            return Response({'error': 'Invalid unit of measurement'}, status=status.HTTP_400_BAD_REQUEST)
        
        if lat_obj and  lng_obj:
            target_point = Point(lat_obj, lng_obj)
            upcoming_events = self.filter_queryset(self.get_queryset()).filter(
            Q(events__point__distance_lte=(target_point, distance)) |
            Q(seminarnformation__point__distance_lte=(target_point, distance)) |
            Q(schoolgym__point__distance_lte=(target_point, distance))
            )
            if not upcoming_events:
                target_point = Point(lat_obj, lng_obj,srid=4326)
                upcoming_events = self.filter_queryset(self.get_queryset()).annotate(distance=GeometryDistance("events__point", target_point)).order_by("distance")[:5]
        else:
            target_point = Point(lat_obj, lng_obj)
            upcoming_events = self.filter_queryset(self.get_queryset()).filter(
                Q(events__point__distance_lte=(target_point, distance)) |
                Q(seminarnformation__point__distance_lte=(target_point, distance)) |
                Q(schoolgym__point__distance_lte=(target_point, distance))
            ).filter(
                (Q(events__start_date__gt=dt.datetime.today()) & Q(events__is_approved=True)) |
                (Q(seminarnformation__start_date__gt=dt.datetime.today()) & Q(seminarnformation__is_approved=True)) |
                (Q(schoolgym__created_at__lte=dt.datetime.today()) & Q(schoolgym__is_approved=True))
            )
        serializer = upcomingEvents_detailsSerializers(upcoming_events, many=True, context={'request': request})
        return Response(serializer.data)




class PastEventsView(viewsets.ModelViewSet):
    serializer_class = upcomingEvents_detailsSerializers
    queryset = all_events_details.objects.all().order_by('-id') 
    filter_backends = [SearchFilter,OrderingFilter,DjangoFilterBackend]
    ordering_fields = ['created_at']
    ordering = ['created_at']
    filterset_fields = ['type']
    # filterset_fields = ['events__online_only','seminarnformation__online_only']
    search_fields = ['events__title','seminarnformation__title','schoolgym__title','events__martial_art_style','seminarnformation__martial_art_style','schoolgym__martial_art_style','events__tags__tag_name','seminarnformation__tags__tag_name','schoolgym__tags__tag_name']

    def get_queryset(self):
        today = dt.datetime.today()
        queryset = all_events_details.objects.filter(
            Q(events__end_date__lte=today) & Q(events__is_approved=True) |
            Q(seminarnformation__end_date__lte=today) & Q(seminarnformation__is_approved=True)
        )
        return queryset

    def list(self, request, format=None):
        lat_obj = float(request.GET.get("lat", None))
        lng_obj = float(request.GET.get("lng", None))
        distance_obj = request.GET.get("distance", None)
        unit = request.GET.get("distance_type", None)
        Judo = request.GET.get('Judo', None)
        online_only = request.GET.get('online_only', None)
        q_Judo = Q()
        if Judo:
            q_Judo = Q(
                Q(Q(events__martial_art_style=Judo) |
                  Q(seminarnformation__martial_art_style=Judo) |
                  Q(schoolgym__martial_art_style=Judo)))
        q_online_only = Q()
        if online_only:
            q_online_only = Q(
                Q(Q(events__online_only=online_only) |
                  Q(seminarnformation__online_only=online_only) |
                  Q(schoolgym__online_only=online_only)))

        if unit == "km":
            if distance_obj:
                distance = D(km=(distance_obj))
            else:
                distance = None
        elif unit == "mi":
            if distance_obj:
                distance = D(mi=(distance_obj))
            else:
                distance = None
        else:
            return Response({'error': 'Invalid unit of measurement'}, status=status.HTTP_400_BAD_REQUEST)

        if lat_obj and lng_obj:
            target_point = Point(lng_obj, lat_obj, srid=4326)
            past_events = self.get_queryset().filter(
                Q(events__point__distance_lte=(target_point, distance)) |
                Q(seminarnformation__point__distance_lte=(target_point, distance)) |
                Q(schoolgym__point__distance_lte=(target_point, distance))
            )
            if not past_events:
                target_point = Point(lng_obj, lat_obj,srid=4326)
                past_events = self.get_queryset().annotate(
                    distance=GeometryDistance("events__point", target_point)).order_by("distance")[:5]

        else:
            target_point = Point(lng_obj, lat_obj,srid=4326)
            past_events = self.get_queryset().filter(
                Q(events__point__distance_lte=(target_point, distance)) |
                Q(seminarnformation__point__distance_lte=(target_point, distance)) |
                Q(schoolgym__point__distance_lte=(target_point, distance))
            ).filter(q_Judo).filter(q_online_only)

        serializer = upcomingEvents_detailsSerializers(past_events, many=True, context={'request': request})
        return Response(data=serializer.data)





class OnGoingEventsView(viewsets.ModelViewSet):
    serializer_class = upcomingEvents_detailsSerializers
    queryset = all_events_details.objects.all().order_by('-id') 
    filter_backends = [SearchFilter,OrderingFilter,DjangoFilterBackend]
    ordering_fields = ['created_at']
    ordering = ['created_at']
    filterset_fields = ['type']
    # filterset_fields = ['events__online_only','seminarnformation__online_only']
    search_fields = ['events__title','seminarnformation__title','schoolgym__title','events__martial_art_style','seminarnformation__martial_art_style','schoolgym__martial_art_style']
    
  
    def list(self, request, format=None):
        Judo = request.GET.get('Judo', None)
        online_only= request.GET.get('online_only', None)
        
        q_Judo = Q()
        if Judo:
            q_Judo = Q(Q(Q(events__martial_art_style=Judo) | Q(seminarnformation__martial_art_style=Judo)| Q(schoolgym__martial_art_style=Judo)))
        q_online_only = Q()
        if online_only:
            q_online_only = Q(Q(Q(events__online_only=online_only)  | Q (seminarnformation__online_only=online_only) | Q (seminarnformation__online_only=online_only) | Q (seminarnformation__online_only=online_only) ))    
        upcoming_events =  self.filter_queryset(self.get_queryset()).filter(Q (events__start_date__lte=dt.datetime.today()) & Q (events__end_date__gte=dt.datetime.today()) & Q (events__is_approved = True)|Q (seminarnformation__start_date__lte=dt.datetime.today())& Q (seminarnformation__end_date__gte=dt.datetime.today()) & Q (seminarnformation__is_approved = True)|Q(schoolgym__created_at__lte=dt.datetime.today())& Q (schoolgym__is_approved = True)).filter(q_Judo ).filter(q_online_only)
        serializer = upcomingEvents_detailsSerializers(upcoming_events, many=True,context={'request':request})
        return Response(serializer.data) 





    



class UploadCsvFileView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        file_extension = file.name.split('.')[-1]
        type1 =  request.data.getlist('type')
        user =  request.data.get('user')
        try:
            user_data = User.objects.get(id=user)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=400)
        if file_extension == 'csv':
            reader = pd.read_csv(file)
        elif file_extension in ['xlsx', 'xls']:
            reader = pd.read_excel(file)
        else:
            return Response({'error': 'Invalid file type'}, status=400)
        
        reader.fillna('', inplace=True) # Replace NaN with empty strings
        for _, row in reader.iterrows():
            try:
                if 'Events' in type1:
                    if file_extension == 'csv':
                        serializer = EventsSerializers(data=row.to_dict())
                        if serializer.is_valid():
                            data_save = serializer.save()
                            data = all_events_details.objects.create(user_id=user, events=data_save, type=type1)
                            data.save()
                        else:
                            return Response(serializer.errors, status=400)
                    else:
                        try:
                            start_date = pd.to_datetime(row[9], format='%Y-%m-%d %H:%M:%S', utc=True).tz_convert(pytz.UTC)
                            if pd.isna(start_date):
                                start_date = None
                            end_date = pd.to_datetime(row[10], format='%Y-%m-%d %H:%M:%S', utc=True).tz_convert(pytz.UTC)
                            if pd.isna(end_date):
                                end_date = None
                        except ValueError as e:
                            print(f"Error processing row {row}: {e}")
                        try:
                            if user_data.role == 0:  # check if the user is admin based on role
                                is_approved = True
                            else:
                                is_approved = False    
                            image_url = row[0]
                            if not image_url.strip():  # check if image_url is empty
                                image_file = None
                            else:
                                image_url_encoded = urllib.parse.quote(image_url, safe=':/')
                                result = urllib.request.urlretrieve(image_url_encoded)
                                image_file = File(open(result[0], 'rb'))
                            new_obj = Events.objects.create(image=image_url,website=row[1],online_registration_link=row[2],event_flyer_material=row[3],event_link=row[4],title=row[5],address=row[6],zip_code=row[7],country=row[8],start_date=start_date,end_date=end_date,time=row[11],contact_first_name=row[12],contact_last_name=row[13],contact_title=row[14],contact_phone_number=row[15],contact_email=row[16],contact_social_media_links=row[17],does_this_event_accept_foreign_participants=row[18],instructions_for_the_event=row[19],related_associations_or_organizations=row[20],online_only=row[21],is_more_information_coming_soon=row[22],comments_by_data_entry_associate=row[23],martial_art_style=row[24],is_approved=is_approved)
                            if image_url:
                                new_obj.image.save(
                                    os.path.basename(image_url),
                                    image_file,
                                )
                            new_obj.save()
                            data = all_events_details.objects.create(user_id=user, events=new_obj, type=type1[0])
                            data.save()
                        except urllib.error.URLError as e:
                            print(f"Error retrieving image from URL {image_url}: {e}")
                        except Exception as e:
                            print(f"Error creating Events object for row {row}: {e}")



                elif 'SeminarInformation' in type1:
                    if file_extension == 'csv':
                        serializer = SeminarSerializers(data=row.to_dict())
                        if serializer.is_valid():
                            sem_data = serializer.save()
                            data = all_events_details.objects.create(user_id=user, events=sem_data, type=type1)
                            data.save()
                        else:
                           return Response(serializer.errors, status=400)
                    else:
                        try:
                            start_date = pd.to_datetime(row[9], format='%Y-%m-%d %H:%M:%S', utc=True).tz_convert(pytz.UTC)
                            if pd.isna(start_date):
                                start_date = None
                            end_date = pd.to_datetime(row[10], format='%Y-%m-%d %H:%M:%S', utc=True).tz_convert(pytz.UTC)
                            if pd.isna(end_date):
                                end_date = None
                        except ValueError as e:
                            print(f"Error processing row {row}: {e}")
                        try:
                            if user_data.role == 0:  # check if the user is admin based on role
                                is_approved = True
                            else:
                                is_approved = False    
                            image_url = row[0]
                            if not image_url.strip():  # check if image_url is empty
                                image_file = None
                            else:
                                image_url_encoded = urllib.parse.quote(image_url, safe=':/')
                                result = urllib.request.urlretrieve(image_url_encoded)
                                image_file = File(open(result[0], 'rb'))
                            new_obj = SeminarInformation.objects.create(image=image_url,website=row[1],online_registration_link=row[2],event_flyer_material=row[3],event_link=row[4],title=row[5],address=row[6],zip_code=row[7],country=row[8],start_date=start_date,end_date=end_date,details=row[11],first_name=row[12],last_name=row[13],comments_by_data_entry_associate=row[14],phone_number=row[15],organizer_email=row[16],social_media_links=row[17],does_this_event_accept_foreign_participants=row[18],special_instructions=row[19],why_is_this_seminar_only_open_to_this_group_of_people=row[20],online_only=row[21],is_more_information_coming_soon=row[22],is_approved=is_approved)
                            if image_url:
                                new_obj.image.save(
                                    os.path.basename(image_url),
                                    image_file,
                                )
                            new_obj.save()
                            data = all_events_details.objects.create(user_id=user, seminarnformation=new_obj, type=type1[0])
                            data.save()    
                        except ValueError as e:
                            print(f"Error processing row {row}: {e}")                                    
                                                                            

                elif 'SchoolGym' in type1:
                    if file_extension == 'csv':
                        serializer = SchoolGymSerializers(data=row.to_dict())
                        if serializer.is_valid():
                            school_data = serializer.save()
                            data = all_events_details.objects.create(user_id=user, events=school_data, type=type1)
                            data.save()
                        else:
                           return Response(serializer.errors, status=400)
                    else:
                        try:
                            start_date = pd.to_datetime(row[9], format='%Y-%m-%d %H:%M:%S', utc=True).tz_convert(pytz.UTC)
                            if pd.isna(start_date):
                                start_date = None
                            end_date = pd.to_datetime(row[10], format='%Y-%m-%d %H:%M:%S', utc=True).tz_convert(pytz.UTC)
                            if pd.isna(end_date):
                                end_date = None
                        except ValueError as e:
                            print(f"Error processing row {row}: {e}")
                        try:
                            if user_data.role == 0:  # check if the user is admin based on role
                                is_approved = True
                            else:
                                is_approved = False    
                            image_url = row[0]
                            if not image_url.strip():  # check if image_url is empty
                                image_file = None
                            else:
                                image_url_encoded = urllib.parse.quote(image_url, safe=':/')
                                result = urllib.request.urlretrieve(image_url_encoded)
                                image_file = File(open(result[0], 'rb'))
                            new_obj = SchoolGym.objects.create(image=image_url,website=row[1],online_registration_link=row[2],event_flyer_material=row[3],event_link=row[4],title=row[5],address=row[6],zip_code=row[7],country=row[8],start_date=start_date,end_date=end_date,time=row[11],contact_first_name=row[12],contact_last_name=row[13],contact_title=row[14],contact_phone_number=row[15],contact_email=row[16],contact_social_media_links=row[17],does_this_event_accept_foreign_participants=row[18],instructions_for_the_event=row[19],related_associations_or_organizations=row[20],online_only=row[21],is_more_information_coming_soon=row[22],comments_by_data_entry_associate=row[23],is_approved=is_approved)
                            if image_url:
                                new_obj.image.save(
                                    os.path.basename(image_url),
                                    image_file,
                                )
                            new_obj.save()
                            data = all_events_details.objects.create(user_id=user, schoolgym=new_obj, type=type1[0])
                            data.save()       
                        except ValueError as e:
                            print(f"Error processing row {row}: {e}") 
                    
                else:
                    return Response({'error': 'Invalid event type'}, status=400)

            except Exception as e:
                error_message = f"Error creating Events object for row {row}: {e}"
                return Response({'error': error_message}, status=400)

        return Response({'success': 'File uploaded successfully'})





def save_image_from_url(model, url):
    r = requests.get(url)

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(r.content)
    img_temp.flush()
    model.image.save("image.jpg", File(img_temp), save=True)



class PageImageView(viewsets.ModelViewSet):
    serializer_class = PageImageSerializers
    queryset = PagesImage.objects.all()


    

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    

    
    

@api_view(['post'])
def generate_haiku(request, word):
    adjectives = ['bright', 'dazzling', 'shining', 'vivid', 'gleaming', 'religious', 'popular', 'traditional', 'cultural', 'available', 'international', 'economic', 'American', 'national', 'different', 'early', 'environmental', 'religious', 'cultural', 'traditional', 'adventurous', 'condescending', 'cooperative', 'courageous', 'despicable', 'determined', 'dilapidated', 'diminutive', 'distressed', 'disturbed']
    nouns = ['sun', 'star', 'moon', 'sky', 'cloud', 'area', 'book', 'business', 'case', 'company', 'family', 'government', 'group', 'home', 'money', 'mother', 'number', 'people', 'place', 'problem', 'program', 'question', 'right', 'room', 'school', 'story', 'student', 'study', 'system', 'thing', 'time', 'water', 'way', 'woman', 'word', 'work', 'world', 'year']

    # Generate the poem using the input word and randomly selected words
    first_line = f"The {word} is a {random.choice(adjectives)} {random.choice(nouns)}.\n"
    second_line = f"{random.choice(['Brightens', 'Illuminates', 'Shines on', 'Lights up', 'Casts a glow on'])} our lives {random.choice(['like', 'as'])} a {random.choice(adjectives)} {word}.\n"
    third_line = f"{random.choice(['Softly rustling in the wind,', 'Natures symphony,', 'The moons silver light,', 'Reflecting on the still lake,', 'Peaceful and quiet,', 'Cherry blossoms bloom,', 'Fleeting beauty of springtime,', 'Ephemeral life,'])}\n"
    
    haiku = f"{first_line}{second_line}{third_line}"
    haiku_lines = haiku.strip().split("\n")
    if len(haiku_lines) != 3:
        # If the haiku doesn't have three lines, return an error
        return Response({"error": "Failed to generate haiku. Please try again."})
    else:
        discussion_type = request.data['discussion_type']
        if discussion_type == 'Poem':
            # If discussion_type is poem, only save poem and user_id
            poem = f"{haiku_lines[0]}\n{haiku_lines[1]}\n{haiku_lines[2]}"
            # Post.objects.create(word=poem, user_id=request.user.id, discussion_type=discussion_type)
            return Response({"poem":poem,"save":True})
        elif discussion_type == 'Both':
            # If discussion_type is both, save all fields including title and thoughts
            title = request.data.get('title')
            thought = request.data.get('thought')
            poem = f"{haiku_lines[0]}\n{haiku_lines[1]}\n{haiku_lines[2]}"
            # Post.objects.create(word=poem, user_id=request.user.id, discussion_type=discussion_type, title=title, thought=thought)
            return Response({"poem":poem, "title":title, "thought":thought})
        else:
            # If discussion_type is invalid, return an error
            return Response({"error": "Invalid discussion_type. Please select either" 'poem'})





        

class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializers
    queryset = Tag.objects.all()   
    filter_backends = [SearchFilter,OrderingFilter,DjangoFilterBackend]
    filterset_fields = ['tag_name']      




class UserbackgroundView(viewsets.ModelViewSet):
    queryset = Userbackgroundimage.objects.all()
    serializer_class = UserbackgroundSerializers

    def create(self, request, *args, **kwargs):
        user = request.user
        user_background, created = Userbackgroundimage.objects.get_or_create(user=user)

        serializer = self.get_serializer(user_background, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    




















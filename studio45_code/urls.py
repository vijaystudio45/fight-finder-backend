from django.urls import path
from . import views
from studio45_code.views import( RegistrationView,
LoginView,
PasswordChange,
ForgetPassword,
ResetPassword,
UpdateUserProfile,
AddBlogViewSet,
contactView,
UserListView,
UserBlocUnblockkView,
# EventViewSet,
VerifyEmail,
AllEventViewSet,
pagesViewSet,
SchoolGymViewSet,
SeminarViewSet,
allModelDataViewSet,
OnlyUserDataView,
UpcomingEventsView,
UploadCsvFileView
# PastEventsView

)

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'AddBlog', AddBlogViewSet)
router.register(r'all_Events', AllEventViewSet)
router.register(r'SchoolGym', SchoolGymViewSet)
router.register(r'Seminar', SeminarViewSet)
router.register(r'pages', pagesViewSet)
router.register(r'all_Model_data', allModelDataViewSet)
router.register(r'user_events', OnlyUserDataView)
router.register(r'upcoming_events', UpcomingEventsView)
router.register(r'past_events', UpcomingEventsView)


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('user-login/', LoginView.as_view(), name='loginview'),
    path('password-change/', PasswordChange.as_view(), name='password_change'),
    path('forget-password/', ForgetPassword.as_view(), name='forget-password'),
    path('reset-password/<token>/<uid>/', ResetPassword.as_view(), name='reset_password'),
    path('update-user-profile/', UpdateUserProfile.as_view(), name='updateuserProfile'),
    path('contact/', contactView.as_view(), name='contact'),
    path('get-user/', UserListView.as_view(), name='get_user'),
    path('UserBlockUnblock/<int:pk>/', UserBlocUnblockkView.as_view(), name='UserBlockUnblock'),
    # path('verify-email/<str:token>/<str:uid>/', VerifyEmail.as_view(), name='verify_email'),
    path('verify-email/<str:uid>/', VerifyEmail.as_view(), name='verify_email'),
    path('user_contact/', views.UserContactView.as_view(), name='user_contact'),
    # path('upcoming_events/', views.UpcomingEventsView.as_view(), name='upcoming_events'),
    path('upcoming_events/<int:pk>/', views.UpcomingEventsViewDetail.as_view(), name='upcoming_events_details'),
    # path('past_events/', views.PastEventsView.as_view(), name='past_events'),
    # path('userdata', views.userDataView.as_view(),name='userdata'),
    # path('upcoming_events_details/', views.UpcomingEventsDetailsView.as_view(), name='upcoming_events_details'),
    path('upload_csv/', UploadCsvFileView.as_view(), name='upload-file')
    
 


    

]

urlpatterns += router.urls 
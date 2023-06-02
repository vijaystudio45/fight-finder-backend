from django.urls import path
# from . import views
from rest_framework import routers
from discussion.views import NotificationPostView,OnlyUserPostView,ThoughtPostView,FollowPostView,GetUserPostView,UserAllDetailView,FollowNewView,followingNewView,savePoemAndBothView,UserPartialUpdateView,SearchHistoryView,allUserView,RemoveFollowAPIView,PostUserView,FollowAPIView,AffiliationView,affiliationSectionView

router = routers.SimpleRouter()
router.register(r'notification_list', NotificationPostView)
router.register(r'only_user_post', OnlyUserPostView)
router.register(r'thought_post', ThoughtPostView)
router.register(r'follow_post', FollowPostView)
router.register(r'user-follower',UserAllDetailView)
router.register(r'savePoemAndBoth',savePoemAndBothView)
router.register(r'users', allUserView)
router.register(r'affiliation_list', AffiliationView)
router.register(r'affiliation_section',affiliationSectionView)









urlpatterns = [
    path('users/<int:user_id>/posts/', GetUserPostView.as_view(), name='user-posts'),
    path('followers/', FollowNewView.as_view(), name='followers'),
    path('following/', followingNewView.as_view(), name='following'),
    path('updateUsers/<int:pk>/', UserPartialUpdateView.as_view(), name='user_partial_update'),
    path('search-history/', SearchHistoryView.as_view()),
    path('remove-follow/<int:follow_id>/', RemoveFollowAPIView.as_view(), name='remove_follow'),
    path('post/<int:post_id>/user/', PostUserView.as_view(), name='post-user'),
    path('follow/', FollowAPIView.as_view(), name='follow'),
   
]
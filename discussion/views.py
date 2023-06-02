from django.http import HttpResponse
from discussion.models import Post,Notification,SearchHistory,Follow,affiliation_section,Affiliation
from studio45_code.models import User,SchoolGym
from .serializers import NotificationPostSerializers,GetOnlyPostSerializers,FollowPostSerializers,UserSerializers,SearchHistorySerializer,UserPartialUpdateSerializer,followTestSerializer,FollowerssssSerializer,FollowingssSerializer,AffiliationSerializer,ThoughtPostSerializers,UserAllSerializer,UserPostSerializer,affiliationSectionSerializers
from rest_framework import viewsets
from django.core.cache import cache
from .serializers  import ThoughtPostSerializers  
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.db.models import Max
from django.db.models import Count
from rest_framework.generics import ListAPIView
from rest_framework import generics
from django.db import IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404



class NotificationPostView(viewsets.ModelViewSet):
    serializer_class = NotificationPostSerializers    
    queryset = Notification.objects.all().order_by('-created_at') 



    def list(self, request):
        following_ids = request.user.follower.all().values_list('follower_id', flat=True)
        following_users = User.objects.filter(id__in=following_ids)
        data = Notification.objects.filter(user__in=following_users)
        latest_following_date = following_users.aggregate(latest=Max('created_at'))['latest']
        if latest_following_date:
            data = data.filter(created_at__gte=latest_following_date)
        data = data.filter(is_seen=False).distinct('post')   
        count = cache.get(f'notification_count_{request.user.id}')
        if count is None:
            count = data.count()
            cache.set(f'notification_count_{request.user.id}', count)
        offset = int(request.GET.get('offset', 0))
        if offset < 0:
            offset = 0
        if offset > count:
            offset = count
        data = data[offset:offset+5]
        serializer = self.get_serializer(data, many=True, context={'request': request, 'count': count})
        return Response(serializer.data)




    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        post_id = request.data.get('post_id')
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            Notification.objects.filter(user=request.user.id,post=post_id).update(is_seen=True)
            context = {
                'message': 'Updated Successfully...',
                'status': status.HTTP_200_OK,
                'errors': serializer.errors,
                'data': serializer.data,
            }
            return Response(context)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        





class ThoughtPostView(viewsets.ModelViewSet):

    serializer_class = ThoughtPostSerializers
    queryset = Post.objects.all().order_by('-created_at')
    filter_backends = [SearchFilter,OrderingFilter,DjangoFilterBackend]
    filterset_fields = ['view_only']



    def list(self, request):
        if request.user.is_anonymous:
            data = Post.objects.all().order_by('-created_at') 
            
        else:
            field_values = self.request.query_params.getlist('view_only', None)
            data = Post.objects.all().order_by('-created_at').exclude(hide_user_post=request.user.id).annotate(num_report_times=Count('report_times')).filter(num_report_times__lte=10)
            if field_values:
                queries = [Q(view_only=value) for value in field_values]
                query = queries.pop()

                for q in queries:
                    query |= q
                data = data.filter(query)
            # return data
        serializer = GetOnlyPostSerializers(data, many=True,context={'request':request}) 
        return Response(serializer.data) 
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            post_instance = serializer.save()
            post_id = post_instance
            follower_ids = request.user.following.all().values_list('follower_id', flat=True)
            notifications = []
            for follower_id in follower_ids:
                notifications.append(Notification(
                    user_id=follower_id,
                    post=post_id,
                    notification=f'{request.user.username} has created a Post',
                    notification_type='Post'
                ))
            Notification.objects.bulk_create(notifications)
            return Response(serializer.data)
        return Response(serializer.errors)

   


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        vote = request.data.get('vote')
        report_times = request.data.get('report_times')

        if vote is not None:
            if request.user in instance.vote.all():
                instance.vote.remove(request.user)
            else:
                instance.vote.add(request.user)
                instance.save(update_fields=[])
            serializer = self.get_serializer(instance)
            return Response({'data': serializer.data})

        if report_times is not None:
            instance.report_times.add(request.user)
            instance.save(update_fields=[])
            serializer = self.get_serializer(instance)
            return Response({'data': serializer.data})

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        context = {
            'message': 'Post Deleted Successfully',
            'status': status.HTTP_204_NO_CONTENT,
            'errors': False,
        }
        return Response(context)   
    



class OnlyUserPostView(viewsets.ModelViewSet):
    serializer_class = ThoughtPostSerializers
    queryset = Post.objects.all().order_by('-created_at') 


    def list(self, request):
        # data = Post.objects.filter(user=request.user.id)
        queryset = self.filter_queryset(self.get_queryset()).filter(user=request.user.id)
        serializer = ThoughtPostSerializers(queryset, many=True,context={'request':request})
        return Response(serializer.data) 
    



class FollowPostView(viewsets.ModelViewSet):
    serializer_class = FollowPostSerializers
    queryset = User.objects.all().order_by('-created_at') 


    def list(self, request):
        queryset = User.objects.annotate(num_follow=Count('follow'))
        serializer = FollowPostSerializers(queryset, many=True,context={'request':request})
        return Response(serializer.data) 
        
    

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        follower_id = request.user.id
        follow_id = request.data.get('follow')

        if follow_id:
            try:
                follower_user = User.objects.get(id=follower_id)
                follow_user = User.objects.get(id=follow_id)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            if instance.follow.filter(id=follower_id).exists():
                instance.follow.remove(follower_user)
                # follower_user.following.remove(instance)
            else:
                instance.follow.add(follower_user)
                # follower_user.following.add(instance)

            instance.save()
            follower_user.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)    
    



class GetUserPostView(ListAPIView):
    serializer_class = ThoughtPostSerializers
    queryset = Post.objects.all()

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        view_only_values = self.request.query_params.getlist('view_only', None)
        queryset = Post.objects.filter(user_id=user_id)
        if view_only_values:
            queryset = queryset.filter(view_only__in=view_only_values)
        return queryset    
    



class allUserView(viewsets.ModelViewSet):
    serializer_class = UserSerializers
    queryset = User.objects.all()  
    filter_backends = [SearchFilter,OrderingFilter,DjangoFilterBackend]
    filterset_fields = ['username']
    search_fields = ['username']


    def get_queryset(self):
        letter = self.request.query_params.get('username', '')
        return User.objects.filter(username__icontains=letter)



class SearchHistoryView(generics.ListAPIView):
    serializer_class = SearchHistorySerializer
    

    def list(self, request, *args, **kwargs):
        queryset = SearchHistory.objects.filter(user=request.user).order_by('-created_at')
        serializer = self.serializer_class(queryset, many=True, context={'request': request})

        for data in serializer.data:
            user_data = User.objects.filter(id=data['query_user_id']).values()
            data['user_data'] = user_data.first() if user_data.exists() else None
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            query = request.data.get('query')
            query_user_id = request.data.get('query_user_id')
            user_id = request.user.id
            data, created = SearchHistory.objects.get_or_create(query=query, user_id=user_id,query_user_id=query_user_id)
            if created:
                context = {
                    'message': '',
                    'status': status.HTTP_201_CREATED,
                    'errors': False,
                }
            else:
                context = {
                    'message': 'Query already exists in history',
                    'status': status.HTTP_200_OK,
                    'errors': False,
                }
            user_data = User.objects.filter(id=query_user_id).values()
            context['user_data'] = user_data.first() if user_data.exists() else None
            return Response(context)    
        except IntegrityError:
            return Response({'error': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)  
        



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserPartialUpdateView(generics.UpdateAPIView):
    serializer_class = UserPartialUpdateSerializer
    queryset = User.objects.all()

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data={'name': '', 'mobile_number': '','primary_number': '','address': '','city': '','state':'','country': '', 'about_me': '','competition_level': '','gender': ''}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        token = get_tokens_for_user(user)
        user_data = serializer.data
        user_data.update({'token': token['access']})
        response_data = user_data
        return Response(response_data, status=status.HTTP_200_OK)
    


class savePoemAndBothView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = ThoughtPostSerializers

    def create(self, request, *args, **kwargs):
        try:
            discussion_type = request.data.get('discussion_type')
            user_id = request.data.get('user_id')
            view_only = request.data.get('view_only')
            word = request.data.get('word')
            thought = request.data.get('thought')
            title = request.data.get('title')
            data=Post.objects.create(discussion_type=discussion_type,user_id=user_id, view_only=view_only,word=word,thought=thought,title=title)
            Notification.objects.create(user=request.user,post=data, notification= f'{request.user.username} has created a poem ',notification_type='Post',)
            serializer = self.get_serializer(data)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)  







class FollowAPIView(generics.GenericAPIView):
    serializer_class = followTestSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        follow_id = request.data.get('follow_id')

        try:
            following_user = User.objects.get(id=follow_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if following_user == request.user:
            return Response({'error': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

        follow, created = Follow.objects.get_or_create(follower=request.user, following=following_user)

        if not created:
            return Response({'error': 'You are already following this user'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'You are now following this user'})

    def delete(self, request, *args, **kwargs):
        follow_id = request.data.get('follow_id')

        try:
            following_user = User.objects.get(id=follow_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        follow = Follow.objects.filter(follower=request.user, following=following_user).first()

        if not follow:
            return Response({'error': 'You are not following this user'}, status=status.HTTP_400_BAD_REQUEST)

        follow.delete()

        return Response({'success': 'You have unfollowed this user'})
    


class FollowNewView(APIView):    
  
    def get(self,request):
        followers = request.user.following.all()
        serializer = FollowerssssSerializer(followers, many=True,context={'request':request})
        return Response(serializer.data)


class followingNewView(APIView):    
  
    def get(self,request):
        following = request.user.follower.all()
        serializer = FollowingssSerializer(following, many=True,context={'request':request})
        return Response(serializer.data)



class UserAllDetailView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAllSerializer



class RemoveFollowAPIView(APIView):
    serializer_class = followTestSerializer

    def delete(self, request, follow_id):
        try:
            following_user = User.objects.get(id=follow_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        follow = Follow.objects.filter(follower=following_user).first()

        if not follow:
            return Response({'error': 'You are not authorized to remove this follow'}, status=status.HTTP_403_FORBIDDEN)

        follow.delete()

        return Response({'success': 'Follow has been removed'})


class PostUserView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = UserPostSerializer

    def get_object(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post.user    
    




class AffiliationView(viewsets.ModelViewSet):
    queryset = Affiliation.objects.all()
    serializer_class = AffiliationSerializer


    def list(self, request):
        # data = Post.objects.filter(user=request.user.id)
        queryset = self.filter_queryset(self.get_queryset()).filter(user=request.user.id)
        serializer = AffiliationSerializer(queryset, many=True,context={'request':request})
        return Response(serializer.data) 
    


    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        martial_arts_type = request.data.get('Martial_Arts_Type')
        number_of_years_practiced = request.data.get('Number_of_Years_practiced')
        rank = request.data.get('Rank')

        # Check if any required fields are missing
        errors = {}
        if not user_id:
            errors['user_id'] = 'This field is required'
        if not martial_arts_type:
            errors['Martial_Arts_Type'] = 'This field is required'
        if not number_of_years_practiced:
            errors['Number_of_Years_practiced'] = 'This field is required'
        if not rank:
            errors['Rank'] = 'This field is required'

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        # Validate the number_of_years_practiced field
        if not number_of_years_practiced.isdigit():
            return Response({'error': 'Invalid value for Number of Years practiced'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if an affiliation record already exists for the user
        affiliation = Affiliation.objects.filter(user_id=user_id).first()

        if affiliation:
            # If an affiliation record exists, update it with the new data
            affiliation.Martial_Arts_Type = martial_arts_type
            affiliation.Number_of_Years_practiced = int(number_of_years_practiced)
            affiliation.Rank = rank
            affiliation.save()
        else:
            # If no affiliation record exists, create a new one
            data = {
                'user_id': user_id,
                'Martial_Arts_Type': martial_arts_type,
                'Number_of_Years_practiced': int(number_of_years_practiced),
                'Rank': rank,
            }
            affiliation = Affiliation.objects.create(**data)

        serializer = self.get_serializer(affiliation)
        return Response(serializer.data)




class affiliationSectionView(viewsets.ModelViewSet):
    queryset = affiliation_section.objects.all()
    serializer_class = affiliationSectionSerializers



    def list(self, request):
        # data = Post.objects.filter(user=request.user.id)
        queryset = self.filter_queryset(self.get_queryset()).filter(user=request.user.id)
        serializer = affiliationSectionSerializers(queryset, many=True,context={'request':request})
        return Response(serializer.data) 


    def create(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('user_id')
            schoolgym_id = request.data.get('schoolgym')
            organization_name = request.data.get('organization_name')
            department_division = request.data.get('department_division')
            contact_person = request.data.get('contact_person')
            contact_email = request.data.get('contact_email')
            contact_phone = request.data.get('contact_phone')
            organization_address = request.data.get('organization_address')
            city = request.data.get('city')
            state_province = request.data.get('state_province')
            purpose_of_affiliation = request.data.get('purpose_of_affiliation')
            affiliation_agreement = request.data.get('affiliation_agreement')
            
            # Check if an affiliation record already exists for the user
            affiliation = affiliation_section.objects.filter(user_id=user_id).first()
            
            if affiliation:

                # If an affiliation record exists, update it with the new data
                affiliation.organization_name = organization_name
                affiliation.department_division = department_division
                affiliation.contact_person = contact_person
                affiliation.organization_address = organization_address
                affiliation.contact_email = contact_email
                affiliation.contact_phone = contact_phone
                affiliation.city = city
                affiliation.state_province = state_province
                affiliation.purpose_of_affiliation = purpose_of_affiliation
                affiliation.affiliation_agreement = affiliation_agreement

                # Get the SchoolGym instance using the ID
                schoolgym = SchoolGym.objects.get(id=schoolgym_id)
                affiliation.schoolgym = schoolgym

                affiliation.save()
            else:
                # If no affiliation record exists, create a new one
                data = {
                    'user_id': user_id,
                    'organization_name': organization_name,
                    'department_division': department_division,
                    'contact_person': contact_person,
                    'organization_address': organization_address,
                    'contact_email': contact_email,
                    'contact_phone': contact_phone,
                    'city': city,
                    'state_province': state_province,
                    'purpose_of_affiliation': purpose_of_affiliation,
                    'affiliation_agreement': affiliation_agreement,
                    'schoolgym': SchoolGym.objects.get(id=schoolgym_id),
                }
                affiliation = affiliation_section.objects.create(**data)
            
            serializer = self.get_serializer(affiliation)
            return Response(serializer.data)
            
        except affiliation_section.DoesNotExist:
            return Response({'error': 'Affiliation record not found'}, status=status.HTTP_404_NOT_FOUND)
        except SchoolGym.DoesNotExist:
            return Response({'error': 'SchoolGym record not found'}, status=status.HTTP_404_NOT_FOUND)
from .models import Post,Notification,SearchHistory,Follow,affiliation_section,Affiliation
from rest_framework import serializers
from studio45_code.models import User



class ThoughtPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__' 


class UserSerializers(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields = '__all__'  

class NotificationPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'        



class FollowPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class GetOnlyPostSerializers(serializers.ModelSerializer):
    user = UserSerializers(required=False)
    class Meta:
        model = Post
        fields = '__all__' 




class SearchHistorySerializer(serializers.ModelSerializer):
    # image_field = SerializerMethodField("get_image_url")
    # image_field = SerializerMethodField()
    # user = UserSerializers(required=False)
    class Meta:
        model = SearchHistory
        fields = '__all__'  

    # def get_image_field(self, obj):
    #     request = self.context.get('request')
    #     return request.build_absolute_uri(obj.user_data.get('profile_image_update', ''))       


    # def get_image_url(self, obj):
    #     request = self.context.get('request')
    #     return request.build_absolute_uri(obj.user.profile_image_update.url)       



class UserPartialUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'





class followTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'




class UserdetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'




class FollowerssssSerializer(serializers.ModelSerializer):
    follower = UserdetSerializer(read_only=True)
    class Meta:
        model = Follow
        fields = ('follower',)




class FollowingssSerializer(serializers.ModelSerializer):
    following = UserdetSerializer(read_only=True)
    
    class Meta:
        model = Follow
        fields = ('following',)



class UserAllSerializer(serializers.ModelSerializer):
    follower = FollowerssssSerializer(source='following.all', many=True)
    following = FollowingssSerializer(source='follower.all', many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'first_name', 'last_name',
                  'profile_image_update', 'is_active', 'name', 'mobile_number',
                  'primary_number', 'mobile_number_verified', 'email_verified',
                  'address', 'city', 'state', 'country', 'forget_password_token',
                  'mobile_verify_token', 'email_verify_token', 'status', 'is_block',
                  'about_me', 'age', 'weight', 'competition_level', 'zip_code',
                  'gender', 'created_at', 'updated_at', 'token_expire_time',
                  'Social_media_links', 'following', 'follower')
        




class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = '__all__'        



class affiliationSectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = affiliation_section
        fields = '__all__' 
from django.db import models
from studio45_code.models import User,SchoolGym





VIEW_TYPE = (
    ('Private', 'Private'),
    ('Public', 'Public'),
    ('Followers', 'Followers'),
    ('School/gym', 'School/gym'),
)


TYPE = (
    ('Poem', 'Poem'),
    ('Post', 'Post'),
    ('Both', 'Both'),
)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="post_user")
    hide_user_post = models.ManyToManyField(User,blank=True,related_name="hide_post_user")
    vote = models.ManyToManyField(User,blank=True,related_name="vote_post_user")
    title = models.CharField(max_length=255,blank=True,null=True)
    discussion_type = models.CharField(default="",max_length=255,choices= TYPE)
    view_only = models.CharField(default= "",max_length=255,choices=VIEW_TYPE)
    thought = models.TextField(null=True,blank=True)
    martial_art_style = models.CharField(max_length=120,null=True,blank=True)
    word = models.CharField(default= "", max_length=100000,null=True,blank=True)
    report_times = models.ManyToManyField(User,blank=True,related_name="report_post_user")
    created_at = models.DateTimeField(auto_now=True, editable=False,null=True,blank=True)
    updated_at =models.DateTimeField(auto_now=True, editable=False,null=True,blank=True)
    modified = models.DateTimeField(auto_now=True, editable=False)





POST_TYPE = (
    ('Post', 'Post'),
)


class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="post_notification")
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    text = models.CharField(max_length=255,null=True,blank=True)
    notification = models.CharField(max_length=255,null=True,blank=True)
    is_seen = models.BooleanField(default=False,null=True,blank=True)
    notification_type = models.CharField(max_length=255,choices=POST_TYPE)
    created_at = models.DateTimeField(auto_now=True, editable=False,null=True,blank=True)





class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    query_user_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    # follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    # following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'
    






class Affiliation(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    Martial_Arts_Type = models.CharField(max_length=255)
    Number_of_Years_practiced = models.IntegerField()
    Rank = models.CharField(max_length=500)






class affiliation_section(models.Model):
    user = models.ForeignKey(User,related_name='affiliation_section',on_delete=models.CASCADE) 
    schoolgym = models.ForeignKey(SchoolGym, on_delete=models.CASCADE,null=True,blank=True)
    organization_name = models.CharField(max_length=255)
    department_division = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    organization_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    purpose_of_affiliation = models.TextField()
    affiliation_agreement = models.BooleanField(max_length=100,null=True,blank=True)
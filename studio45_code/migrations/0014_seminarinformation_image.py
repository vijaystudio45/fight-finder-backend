# Generated by Django 4.1.4 on 2023-01-13 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studio45_code', '0013_alter_user_profile_image_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='seminarinformation',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='Seminar_images/'),
        ),
    ]

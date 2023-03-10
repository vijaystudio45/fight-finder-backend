# Generated by Django 4.1.4 on 2023-01-16 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studio45_code', '0016_schoolgym_image_seminarinformation_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='created',
        ),
        migrations.AddField(
            model_name='events',
            name='created_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='events',
            name='updated_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='schoolgym',
            name='created_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='schoolgym',
            name='updated_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='seminarinformation',
            name='created_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='seminarinformation',
            name='updated_at',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]

# Generated by Django 4.1.4 on 2023-01-16 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studio45_code', '0017_remove_events_created_events_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='all_events_details',
            name='created_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='all_events_details',
            name='updated_at',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]

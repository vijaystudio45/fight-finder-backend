# Generated by Django 4.1.4 on 2023-01-19 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studio45_code', '0022_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]

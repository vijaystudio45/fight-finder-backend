# Generated by Django 4.1.4 on 2023-01-19 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studio45_code', '0021_alter_user_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default=1, max_length=100, verbose_name='username'),
            preserve_default=False,
        ),
    ]
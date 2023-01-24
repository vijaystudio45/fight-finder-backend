# Generated by Django 4.1.4 on 2023-01-10 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studio45_code', '0002_alter_pages_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pages',
            name='created_at',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='pages',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pages',
            name='updated_at',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]

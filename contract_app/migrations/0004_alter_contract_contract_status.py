# Generated by Django 4.1.4 on 2022-12-16 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract_app', '0003_alter_contract_contract_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='contract_status',
            field=models.BooleanField(default=0),
        ),
    ]

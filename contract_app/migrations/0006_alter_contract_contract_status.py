# Generated by Django 4.1.4 on 2022-12-20 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract_app', '0005_alter_billing_contract_alter_company_contract_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='contract_status',
            field=models.IntegerField(),
        ),
    ]

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import *






class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = '__all__'     



class ContractSerializer(serializers.ModelSerializer):
    contract_persons=PersonSerializer(many=True, required=False)
    contract_companies=CompanySerializer(many=True, required=False)
    contract_products=ProductSerializer(many=True, required=False)
    contract_billing=BillingSerializer(many=True, required=False)
    
    class Meta:
        model = Contract
        fields = '__all__'
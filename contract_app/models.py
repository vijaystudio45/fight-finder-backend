from django.db import models

# Create your models here.

PRODUCT_TYPE = [
    ("digital", "digital"),
    ("analogous", "analogous"),
    ("service", "service")
]


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
     abstract = True
  

class Contract(BaseModel):
    contract_name = models.CharField(max_length=50)
    contract_status = models.IntegerField()
    last_step = models.CharField(max_length=100)
    note = models.CharField(max_length=50, null=True, blank=True)
    

class Person(BaseModel):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE,blank=True,null=True,related_name='contract_persons')
    first_name = models.CharField(max_length=30,blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
   

class Company(BaseModel):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE,blank=True,null=True,related_name='contract_companies')
    Company_name = models.CharField(max_length=255,blank=True, null=True) 


class Product(BaseModel):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE,blank=True,null=True,related_name='contract_products')
    product_name = models.CharField(max_length=255,blank=True, null=True)
    product_type = models.CharField(max_length=100, choices=PRODUCT_TYPE)


class Billing(BaseModel):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE,blank=True,null=True,related_name='contract_billing')
    billing_number = models.IntegerField(blank=True, null=True)
    billing_date = models.DateField(blank=True, null=True)
    billing_amount = models.IntegerField(blank=True, null=True)

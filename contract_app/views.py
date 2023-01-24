from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from contract_app.serializers import (
    ContractSerializer,
    PersonSerializer,
    CompanySerializer,
    ProductSerializer,
    BillingSerializer,
)
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.

class ContractViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        if instance.contract_status == 1:
            return Response({'message': "you are not updated this user"})
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            context = {
                'message': 'Updated Successfully...',
                'status': status.HTTP_200_OK,
                'errors': serializer.errors,
                'data': serializer.data,
            }
            return Response(context)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['contract',]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        if instance.contract.contract_status == True:
            return Response({'message': "you are not updated this user"})
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            context = {
                'message': 'Updated Successfully...',
                'status': status.HTTP_200_OK,
                'errors': serializer.errors,
                'data': serializer.data,
            }
            return Response(context)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['contract',]


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        if instance.contract.contract_status == True:
            return Response({'message': "you are not updated this user"})
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            context = {
                'message': 'Updated Successfully...',
                'status': status.HTTP_200_OK,
                'errors': serializer.errors,
                'data': serializer.data,
            }
            return Response(context)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['contract',]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        if instance.contract.contract_status == True:
            return Response({'message': "you are not updated this user"})
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            context = {
                'message': 'Updated Successfully...',
                'status': status.HTTP_200_OK,
                'errors': serializer.errors,
                'data': serializer.data,
            }
            return Response(context)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)    




class BillingViewSet(viewsets.ModelViewSet):
    serializer_class = BillingSerializer
    queryset = Billing.objects.all() 
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['contract',]       


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        if instance.contract.contract_status == True:
            return Response({'message': "you are not updated this user"})
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            context = {
                'message': 'Updated Successfully...',
                'status': status.HTTP_200_OK,
                'errors': serializer.errors,
                'data': serializer.data,
            }
            return Response(context)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




        




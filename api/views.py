#from django.shortcuts import render
from django.conf import settings
import pandas as pd
from rest_framework import generics
from django.urls import reverse_lazy
from .models import ExcelFileUpload, Clients, Products, Bills, BillsProducts
from .serializers import ClientSerializer, ProductSerializer, BillSerializer, BillsProductSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
import uuid


#Client List and Create
class clients(generics.ListCreateAPIView):
    queryset = Clients.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)

#Client Update and Delete 
class clientsUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Clients.objects.all()
    serializer_class = ClientSerializer
    lookup_fields = ['id']
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)

#Products List and Create
class Product(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)

#Products Update and Delete
class ProductsUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_fields = ['id']
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)

#Bills List and Create
class Bill(generics.ListCreateAPIView):
    queryset = Bills.objects.all()
    serializer_class = BillSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)

    
#Bills Update and Delete
class BillsUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bills.objects.all()
    serializer_class = BillSerializer
    lookup_fields = ['id']
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)

#BillsProducts List and Create
class BillProducts(generics.ListCreateAPIView):
    queryset = BillsProducts.objects.all()
    serializer_class = BillsProductSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)

#BillsProducts Update and Delete
class BillsProductsUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = BillsProducts.objects.all()
    serializer_class = BillsProductSerializer
    lookup_fields = ['id']
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)   


class ExportImportExcel(APIView):

    def get(self, request):
        clients_obj = Clients.objects.all()
        serializer = ClientSerializer(clients_obj, many=True)
        df = pd.DataFrame(serializer.data)
        df.to_csv(f"static/excel/{uuid.uuid4()}.csv", encoding="UTF-8", index=False)
        return Response({'status':200})

    def post(self, request):
        excel_upload_obj = ExcelFileUpload.objects.create(excel_file_upload=request.FILES['files'])
        df = pd.read_csv(f"{settings.BASE_DIR}/{excel_upload_obj.excel_file_upload}")
        print(df.values.tolist())
        for x in (df.values.tolist()):
            Clients.objects.create(
                document= x[0],
                first_name = x[1],
                last_name = x[2],
                email= x[3]
            )
        return Response({'status':200})


class Login(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = _url = reverse_lazy('client_list')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, *kwargs)

    def form_valid(self,form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        token,_ = Token.objects.get_or_create(user=user)
        if token:
            login(self.request, form.get_user())
            return super(Login,self).form_valid(form)


class Logout(APIView):

    def get(self, request, *args, **kwargs):

        request.user.auth_token.delete()
        logout(request)
        return Response({'result: YOU ARE LOGGED OUT': True})
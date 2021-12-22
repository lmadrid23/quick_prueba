from django.urls import path
from .views import clients, Product, Bill, BillProducts, clientsUpdateDelete
from .views import ExportImportExcel, ProductsUpdateDelete, BillsUpdateDelete, BillsProductsUpdateDelete
from api import views

urlpatterns = [
    path('client/', clients.as_view(), name='client_list'),
    path('client/ud/<pk>', clientsUpdateDelete.as_view(), name='client_ud'),
    path('products/', Product.as_view(), name='product_list'),
    path('products/ud/<pk>', ProductsUpdateDelete.as_view(), name='product_ud'),
    path('bills/', Bill.as_view(), name='bill_list'),
    path('bills/ud/<pk>', BillsUpdateDelete.as_view(), name='bills_ud'),
    path('bills/products/', BillProducts.as_view(), name='bill_list'),
    path('bills/products/ud/<pk>', BillsProductsUpdateDelete.as_view(), name='bills_product_ud'),
    path('excel/',ExportImportExcel.as_view()),
]
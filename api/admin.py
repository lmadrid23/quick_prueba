from django.contrib import admin

from .models import Clients, Products, Bills, BillsProducts

admin.site.register(Clients)
admin.site.register(Products)
admin.site.register(Bills)
admin.site.register(BillsProducts)
from django.contrib import admin
from django.urls import path,include
from app.views import *

urlpatterns = [
    path('export_data_to_excel/', export_data_to_excel),
    path('', import_data_to_db),
    path("admin/", admin.site.urls),
    path('', include('optimizer.urls')),  # Adjust as per your app name


]

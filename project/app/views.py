from django.shortcuts import render
from .models import *
import pandas as pd
from django.http import JsonResponse
from django.conf import settings


def export_data_to_excel(request):
    # Retrieve all Employee objects from the database
    objs = GFG.objects.all()
    data = []
    for obj in objs:
        data.append({
            "name": obj.name,
            "contact": obj.contact,
            "address": obj.address
        })
    pd.DataFrame(data).to_excel('output.xlsx')
    return JsonResponse({
        'status': 200
    })


def import_data_to_db(request):
    data_to_display = None
    if request.method == 'POST':
        file = request.FILES['files']
        obj = File.objects.create(
            file=file
        )

        path = file.file
        df = pd.read_excel(path)
        data_to_display = df.to_html()

    return render(request, 'excel.html', {'data_to_display': data_to_display})

# views.py

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import pandas as pd
import folium
from geopy.distance import distance
from itertools import permutations
from .route_optimizer import RouteOptimizer

def upload_excel(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        uploaded_file_url = fs.url(filename)

        # File path of the uploaded Excel file
        file_path = os.path.join(settings.MEDIA_ROOT, filename)

        # Define coordinates and waypoints (example)
        coordinates = {
            'DET Jemmal': (35.62204947080937, 10.737054111955766),
            'Hotel Mövenpick': (35.44223136826162, 10.72312365515618),
            'Haupteingang DRX METS': (35.787911659580985, 10.665566994799278),
            'airport TUN': (35.62204947080937, 10.737054111955766),
            'SA': (36.08916308099261, 9.352583816862902),
            'KA': (35.716133827775174, 10.115782222185778),
            'DE': (36.429232097114486, 10.120401402608953),
            # Add more locations as needed
        }
        start_points = ['Hotel Mövenpick', 'SA']
        waypoints = ['Haupteingang DRX METS', 'KA']
        end_points = ['airport TUN', 'DE']

        # Specify the columns to read from the Excel file
        columns_to_read = ['Text', 'Persons']

        # Create RouteOptimizer instance and process data
        optimizer = RouteOptimizer(file_path, columns_to_read, coordinates, start_points, waypoints, end_points)
        optimizer.read_excel_columns()
        optimizer.process_data()
        optimizer.find_shortest_paths()
        optimizer.generate_maps()

        # Get list of generated map files to display in template
        maps = []
        for idx, (shortest_path, total_distance) in enumerate(optimizer.shortest_paths):
            map_url = os.path.join(settings.MEDIA_URL, f"maps/map_{idx + 1}.html")
            maps.append(map_url)

        return render(request, 'optimizer/upload_excel.html', {
            'uploaded_file_url': uploaded_file_url,
            'maps': maps,
        })

    return render(request, 'optimizer/upload_excel.html')

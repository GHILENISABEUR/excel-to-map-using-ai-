import pandas as pd
import folium
from geopy.distance import distance
from itertools import permutations

class RouteOptimizer:
    def __init__(self, file_path, columns, coordinates, start_points, waypoints, end_points):
        self.file_path = file_path
        self.columns = columns
        self.coordinates = coordinates
        self.start_points = start_points
        self.waypoints = waypoints
        self.end_points = end_points
        self.df = None
        self.all_locations = None
        self.distances = {}
        self.shortest_paths = []

    def read_excel_columns(self):
        try:
            df = pd.read_excel(self.file_path)
            missing_columns = [col for col in self.columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Columns '{', '.join(missing_columns)}' not found in the Excel file.")
            self.df = df[self.columns]
        except Exception as e:
            print(f"Error reading the Excel file: {e}")
            self.df = None

    def process_data(self):
        if self.df is not None:
            self.df[['Depart', 'Destination']] = self.df['Text'].str.split(' to ', n=1, expand=True)
            self.df.dropna(inplace=True)
            self.all_locations = set(self.df['Depart'].tolist() + self.df['Destination'].tolist())
            self.compute_distances()

    def compute_distances(self):
        for loc1 in self.all_locations:
            for loc2 in self.all_locations:
                if loc1 != loc2 and loc1 in self.coordinates and loc2 in self.coordinates:
                    self.distances[(loc1, loc2)] = distance(self.coordinates[loc1], self.coordinates[loc2]).km

    def find_shortest_paths(self):
        valid_locations = [loc for loc in self.all_locations if loc in self.coordinates]
        remaining_locations = [loc for loc in valid_locations if loc not in self.start_points + self.waypoints + self.end_points]

        self.shortest_paths = []
        for start in self.start_points:
            for end in self.end_points:
                for perm in permutations(remaining_locations):
                    path = [start] + list(perm) + self.waypoints + [end]
                    total_distance = sum(self.distances.get((path[i], path[i+1]), float('inf')) for i in range(len(path) - 1))
                    self.shortest_paths.append((path, total_distance))

        self.shortest_paths.sort(key=lambda x: x[1])

    def generate_maps(self):
        for idx, (shortest_path, total_distance) in enumerate(self.shortest_paths):
            optimized_coordinates = [self.coordinates[loc] for loc in shortest_path]
            m = folium.Map(location=[optimized_coordinates[0][0], optimized_coordinates[0][1]], zoom_start=10)

            for i in range(len(shortest_path) - 1):
                depart_condition = self.df['Depart'] == shortest_path[i]
                dest_condition = self.df['Destination'] == shortest_path[i+1]
                if len(self.df.loc[depart_condition & dest_condition]) > 0:
                    persons_info = self.df.loc[depart_condition & dest_condition, 'Persons'].values[0]
                    folium.Marker(optimized_coordinates[i+1], popup=f'Coordinates: {optimized_coordinates[i+1]}<br>Persons: {persons_info}').add_to(m)
                else:
                    print(f"No data found for journey from {shortest_path[i]} to {shortest_path[i+1]}")
            folium.PolyLine(locations=optimized_coordinates, color='blue').add_to(m)
            m.save(f"maps/map_{idx + 1}.html")  # Adjust the directory if necessary

    def print_debug_info(self):
        if self.shortest_paths:
            for path, total_distance in self.shortest_paths:
                print("Shortest Path:", path)
                print("Unique Departs:", set(self.df['Depart']))
                print("Unique Destinations:", set(self.df['Destination']))
                print(f"Optimized path: {' -> '.join(path)}")
                print(f"Total distance: {total_distance} km")

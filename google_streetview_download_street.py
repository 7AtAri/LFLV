import requests
import os
import polyline
import geopy.distance
from geopy.distance import geodesic, distance, great_circle
from geopy import Point
import math
import config

folder="images_fav_40_pitch_20"
os.makedirs(folder, exist_ok=True)  # Create the images directory

''' this code does:
    1) Get the coordinates of two intersections on a street using the Google Geocoding API.
    2) Use the Google Directions API to obtain a route between these two intersections.
    3) Interpolate points along this route at specified intervals.
    4) Use the Google Street View API to download images at each of these points.
'''

def get_coordinates(street, city, api_key):
    """Get coordinates of a street in a city using Google Geocoding API."""
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={street},+{city}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200 and 'results' in response.json():
        results = response.json()['results']
        if results:
            location = results[0]['geometry']['location']
            return location['lat'], location['lng']
    return None, None

# improved version of get_coordinates:
def get_coordinates_imp(street, city, api_key):
    """Get coordinates of a street in a city using Google Geocoding API."""
    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={street},+{city}&key={api_key}"
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for 4xx/5xx responses
        data = response.json()
        
        if data.get('status') == 'OK':
            results = data.get('results', [])
            if results:
                location = results[0]['geometry']['location']
                return location['lat'], location['lng']
            else:
                print("No results found for the given location.")
        else:
            print(f"Error in Geocoding API response: {data.get('status')}, {data.get('error_message', 'No error message')}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coordinates: {e}")

    return None, None


def get_route(start_point, end_point, api_key):
    """Get route between two points using Google Directions API."""
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start_point}&destination={end_point}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200 and 'routes' in response.json():
        routes = response.json()['routes']
        if routes:
            # Extract the polyline for the first route
            return polyline.decode(routes[0]['overview_polyline']['points'])
        else:
            print("No routes found.")
    else:
        print("An error occurred.")
    return []

# improved version of get_route:
def get_route_imp(start_point, end_point, api_key, waypoints):
    """Get route between two points using Google Directions API."""
    try:
        waypoints_param = '|'.join([f"via:{lat},{lon}" for lat, lon in waypoints]) 
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start_point}&destination={end_point}&avoid=highways&mode=walking&waypoints={waypoints_param}&key={api_key}"
        #url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start_point}&destination={end_point}&mode=walking&key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        routes = response.json().get('routes', [])
        if routes:
            return polyline.decode(routes[0]['overview_polyline']['points'])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching route: {e}")
    return []


def calculate_points(start_coord, end_coord, step=0.001):
    """Generate points between two coordinates.
        --> not needed anymore
    """
    points = []
    start = geopy.Point(start_coord)
    end = geopy.Point(end_coord)
    distance = geopy.distance.distance(start, end).km
    steps = int(distance / step)
    d = geopy.distance.distance(kilometers=step)
    for i in range(steps):
        point = d.destination(point=start, bearing=d.bearing(start, end))
        points.append((point.latitude, point.longitude))
        start = point
    return points


def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculate the bearing between two points.
    The formulae used is the following:
    θ = atan2(sin(Δlong).cos(lat2), cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise ValueError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2() returns values from -π to +π (−180° to +180°)
    # so we need to normalize the result by converting it to a compass bearing (0° to 360°)
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def interpolate_points(points, distance_meters):
    """Interpolate points along the route at specified intervals in meters."""
    interpolated_points = []
    for i in range(len(points) - 1):
        start = Point(points[i])
        end = Point(points[i + 1])

        while True:
            interpolated_points.append((start.latitude, start.longitude))
            segment = geodesic((start.latitude, start.longitude), (end.latitude, end.longitude))
            if segment.meters <= distance_meters:
                break
            bearing_to_end = calculate_initial_compass_bearing((start.latitude, start.longitude), (end.latitude, end.longitude))
            start = geodesic(kilometers=distance_meters / 1000.0).destination(point=start, bearing=bearing_to_end)

    # Add the last point
    interpolated_points.append((end.latitude, end.longitude))
    return interpolated_points



def download_street_view_images(api_key, points):
    for i, (lon, lat) in enumerate(points):
        try:
            url = f"https://maps.googleapis.com/maps/api/streetview?size=400x400&location={lat},{lon}&key={api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                # Additional checks can be added here to verify the content of the response
                file_path = os.path.join("images", f"image_{i}.jpg")
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                    print(f"Downloaded {file_path}")
            else:
                print(f"No image available at {lat}, {lon}")
        except Exception as e:
            print(f"An error occurred: {e}")

# improved version of download_street_view_images:
def download_street_view_images_360(api_key, points):
    """Download 360-degree images at each point."""
    for i, (lat, lon) in enumerate(points):
        for heading in [0, 90, 180, 270]:  # North, East, South, West
            try:
                # fov is hardcoded here:
                # fov=90 in url sets the field of view to 90 degrees, which provides a relatively wide-angle view.  A smaller value -> more zoomed-in, larger value (max fov=120) -> wider view.
                url = f"https://maps.googleapis.com/maps/api/streetview?size=400x400&location={lat},{lon}&heading={heading}&fov=40&pitch=20&key={api_key}"
                response = requests.get(url)
                response.raise_for_status()  # Check for HTTP errors
                file_path = os.path.join(folder, f"image_{i}_heading_{heading}.jpg")
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                    print(f"Downloaded {file_path}")
            except requests.exceptions.RequestException as e:
                print(f"Error downloading image at {lat}, {lon} with heading {heading}: {e}")




API_KEY = config.google_api_key  # Your API key here
CITY = 'Las Vegas'
STREET = 'Las Vegas Boulevard'
START_INTERSECTION = 'Sahara Avenue'
END_INTERSECTION =  'Russell Road'
INTERVAL_METERS = 61  # Distance between points in meters


# Get coordinates of intersections
start_lat, start_lon = get_coordinates_imp(f"{STREET} and {START_INTERSECTION}", CITY, API_KEY)
end_lat, end_lon = get_coordinates_imp(f"{STREET} and {END_INTERSECTION}", CITY, API_KEY)
#waypoint1_lat, waypoint1_lon = get_coordinates_imp(f"{STREET} and Mandala Bay Road", CITY, API_KEY)
#waypoint2_lat, waypoint2_lon = get_coordinates_imp(f"{STREET} and Paris Drive", CITY, API_KEY)

sahara=(36.142076, -115.157606)
circus_circus=(36.138817, -115.166408)
venice=(36.123644, -115.169367)
cesars_palace=(36.117576, -115.173490)
paris_drive=(36.111743, -115.171362)
bellagio_drive=(36.112280, -115.174795)
new_york_new_york=(36.101861, -115.175843)
excalibur=(36.100318, -115.175263)
luxor_drive=(36.095613, -115.174510)

waypoints=[sahara, circus_circus, venice, cesars_palace, paris_drive, bellagio_drive, new_york_new_york, excalibur, luxor_drive]
if start_lat and end_lat:
    route = get_route_imp(f"{start_lat},{start_lon}", f"{end_lat},{end_lon}", API_KEY, waypoints)
    if route:
        points = interpolate_points(route, INTERVAL_METERS)
        print(points)
        download_street_view_images_360(API_KEY, points)
    else:
        print("Could not retrieve a valid route.")
else:
    print("Could not find coordinates for the specified intersections.")




'''
Potential Issues and Considerations:

    API Key Restrictions: Ensure that the API key is unrestricted or
                                        properly restricted to allow calls to the Geocoding, Directions, and Street View APIs.

    Error Handling: The script should handle possible errors, such as network issues, 
                            API rate limits, or no data available for a specific location.

    Route Complexity: The actual route might be complex, 
                                    especially in urban areas with many turns or one-way streets. 
                                    The polyline returned by the Directions API is an overview 
                                    and might simplify some of these complexities.

'''
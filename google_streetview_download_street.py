import requests
import os
import polyline
import geopy.distance

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
        results = response.json().get('results', [])
        if results:
            location = results[0]['geometry']['location']
            return location['lat'], location['lng']
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
def get_route_impr(start_point, end_point, api_key):
    """Get route between two points using Google Directions API."""
    try:
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start_point}&destination={end_point}&key={api_key}"
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

def interpolate_points(points, distance_meters):
    """Interpolate points along the route at specified intervals in meters."""
    interpolated_points = []
    for i in range(len(points) - 1):
        start = geopy.Point(points[i])
        end = geopy.Point(points[i + 1])
        d = geopy.distance.distance(kilometers=distance_meters / 1000.0)

        while start.distance(end) > distance_meters:
            interpolated_points.append((start.latitude, start.longitude))
            start = d.destination(point=start, bearing=d.bearing(start, end))

    interpolated_points.append((end.latitude, end.longitude))  # Add the last point
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
                url = f"https://maps.googleapis.com/maps/api/streetview?size=400x400&location={lat},{lon}&heading={heading}&fov=90&key={api_key}"
                response = requests.get(url)
                response.raise_for_status()  # Check for HTTP errors
                file_path = os.path.join("images", f"image_{i}_heading_{heading}.jpg")
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                    print(f"Downloaded {file_path}")
            except requests.exceptions.RequestException as e:
                print(f"Error downloading image at {lat}, {lon} with heading {heading}: {e}")


API_KEY = 'YOUR_API_KEY'
CITY = 'Your City'
STREET = 'Main Street'
START_INTERSECTION = 'First Street'
END_INTERSECTION = 'Second Street'
INTERVAL_METERS = 50  # Distance between points in meters

# Get coordinates of intersections
start_lat, start_lon = get_coordinates(f"{STREET} & {START_INTERSECTION}", CITY, API_KEY)
end_lat, end_lon = get_coordinates(f"{STREET} & {END_INTERSECTION}", CITY, API_KEY)

if start_lat and end_lat:
    route = get_route(f"{start_lat},{start_lon}", f"{end_lat},{end_lon}", API_KEY)
    if route:
        points = interpolate_points(route, INTERVAL_METERS)
        download_street_view_images(API_KEY, points)
    else:
        print("Could not retrieve a valid route.")
else:
    print("Could not find coordinates for the specified intersections.")




'''
Potential Issues and Considerations:

    API Key Restrictions: Ensure that the API key is unrestricted or properly restricted to allow calls to the Geocoding, Directions, and Street View APIs.

    Error Handling: The script should handle possible errors, such as network issues, API rate limits, or no data available for a specific location.

    Route Complexity: The actual route might be complex, especially in urban areas with many turns or one-way streets. The polyline returned by the Directions API is an overview and might simplify some of these complexities.

    API Quotas and Costs: Frequent or numerous requests to these APIs may result in charges or hitting usage quotas.

    Dependencies: Ensure all required libraries (requests, polyline, geopy) are installed.

    Testing: It's essential to test the script with real-world examples to ensure it behaves as expected, especially for handling intersections and generating routes.
'''
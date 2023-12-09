# this code 
# - downloads all images in a bounding box from Mapillary
# - groups images by sequence ID
# - saves images to a folder named by sequence ID
# - saves images with image ID as filename
# 
# code adapted from:
# https://gist.github.com/cbeddow/79d68aa6ed0f028d8dbfdad2a4142cf5
#
import mercantile
import mapbox_vector_tile
import requests
import json
import os
from vt2geojson.tools import vt_bytes_to_geojson
    
# define an empty geojson as output
output= { "type": "FeatureCollection", "features": [] }

# vector tile endpoints -- change this in the API request to reference the correct endpoint
tile_coverage = 'mly1_public'    # image access point

# tile layer depends which vector tile endpoints: 
# 1. if map features or traffic signs, it will be "point" always
# 2. if looking for coverage, it will be "image" for points, "sequence" for lines, or "overview" for far zoom
tile_layer = "image"          

# Mapillary access token -- user should provide their own
access_token = 'MLY|6919611378086321|feb37f9b9d4e6dc4ca37b7a6a862f43c'

# a bounding box in [east_lng,_south_lat,west_lng,north_lat] format
# west, south, east, north = [-115.150331, 36.085134 , -115.183582, 36.150943]
west, south, east, north = [-115.198081, 36.094581 , -115.212071, 36.105747]

# get the list of tiles with x and y coordinates which intersect our bounding box
# MUST be at zoom level 14 where the data is available, other zooms currently not supported

#tiles = list(mercantile.tiles(west, south, east, north, 14)) # prepare the tiles
tiles = list(mercantile.tiles(west, south,east, north, 14)) # prepare the tiles

#print("Number of tiles: ", len(tiles))
# loop through list of tiles to get tile z/x/y to plug in to Mapillary endpoints and make request
for k,tile in enumerate(tiles):
    tile_url = 'https://tiles.mapillary.com/maps/vtp/{}/2/{}/{}/{}?access_token={}'.format(tile_coverage,tile.z,tile.x,tile.y,access_token) # prep the url
    response = requests.get(tile_url) # access the api
    print(response.status_code)
    print(response.content)
    data = vt_bytes_to_geojson(response.content, tile.x, tile.y, tile.z,layer=tile_layer)  # convert the response to geojson
    
    # push to output geojson object if yes
    for i,feature in enumerate(data['features']):
        #print("feature nr: ", i)
        # get lng,lat of each feature
        lng = feature['geometry']['coordinates'][0]     
        lat = feature['geometry']['coordinates'][1]
        
        # ensure feature falls inside bounding box since tiles can extend beyond
        if lng > west and lng < east and lat > south and lat < north:
            print("feature in bounding box")
            # create a folder for each unique sequence ID to group images by sequence
            sequence_id = feature['properties']['sequence_id']
            image_folder_path = "/Users/ari/Documents/Data_Science/3_semester/learning_from_las_vegas/LFLV/images/"
            sequence_folder_path = os.path.join(image_folder_path, sequence_id)

            if not os.path.exists(sequence_folder_path):
                os.makedirs(sequence_folder_path)

            # request the URL of each image
            image_id = feature['properties']['id']
            header = {'Authorization' : 'OAuth {}'.format(access_token)}
            url = 'https://graph.mapillary.com/{}?fields=thumb_2048_url'.format(image_id)
            r = requests.get(url, headers=header)
            data = r.json()
            image_url = data['thumb_2048_url']

            # save each image with ID as filename to directory by sequence ID
            with open('{}/{}.jpg'.format(sequence_id, image_id), 'wb') as handler:
                image_data = requests.get(image_url, stream=True).content
                handler.write(image_data)
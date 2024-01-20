### other explored approaches that did not work properly:

- google image search package:
  * https://pypi.org/project/GoogleImageScraper/
  * https://www.wikihow.com/Download-an-Image-from-Google-Maps
    
- mapillary image download via API:
  * token: MLY|6919611378086321|feb37f9b9d4e6dc4ca37b7a6a862f43c
  * client ID: 6919611378086321 
  * https://github.com/pyramid3d/python-tools/blob/master/src/mapillary_download.py  -> date and driver
  * https://gist.github.com/cbeddow/79d68aa6ed0f028d8dbfdad2a4142cf5
  * https://pypi.org/project/mapillary/#possible-issues
    
    latitude(nord-süd)-longitude(ost-west)
    
     1) 36.085134, -115.183582 (links, west, unten,south)
     2) 36.087295, -115.147327 (rechts, east, unten, south)
     3) 36.150943, -115.184663 (links, west, oben, north)
     4) 36.150943, -115.150331 (rechts, east, oben, north)

   -> bounding box: [-115.150331, 36.085134 , -115.183582, 36.150943]
                    [east_lat, south_lat, west_lng, north_lat]

     smaller test piece (additionally):
  
     1) 36.094720, -115.198081 (rechts, east, unten, south)
     2) 36.094581, -115.211899 (links, west, unten,south)
     3) 36.105192, -115.212071 (links, west, oben, north)
     4) 36.105747, -115.200055 (rechts, east, oben, north)
  
     -> bounding box: [-115.198081, 36.094581 , -115.212071, 36.105747]
  
  
  * https://www.mapillary.com/developer/api-documentation?locale=de_DE#image
    

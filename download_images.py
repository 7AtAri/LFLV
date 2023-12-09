

import mapillary.interface as mly
import requests
import json


# Your token here!
# To get one, visit https://www.mapillary.com/dashboard/developer, go to 'developers',
# Then 'register application', register a new application (read access atleast),
# then copy & paste the 'Client Token' here
MLY_ACCESS_TOKEN = 'MLY|6919611378086321|feb37f9b9d4e6dc4ca37b7a6a862f43c'

mly.set_access_token(MLY_ACCESS_TOKEN)

data = mly.get_image_close_to(
    longitude=31, latitude=30, radius=2000, image_type="flat"
).to_dict()

with open("get_image_close_to.json", mode="w") as f:
    json.dump(data, f, indent=4)
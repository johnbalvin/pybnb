# Airbnb scraper in Python

## Overview
This project is an open-source tool developed in Python for extracting product information from Airbnb. It's designed to be easy to use, making it an ideal solution for developers looking for Airbnb product data.

## Features
- Full search support
- Extracts detailed product information from Airbnb
- Implemented in Python just because it's popular
- Easy to integrate with existing Python projects
- The code is optimize to work on this format: ```https://www.airbnb.com/rooms/[roomID]```

### Install

```bash
$ pip install gobnb
```
## Examples

```Python
import gobnb
import json
currency="MXN"
check_in = "2024-03-11"
check_out = "2024-03-14"
ne_lat = -1.1225978433925647
ne_long = -77.59713412765507
sw_lat = -1.03866277790021
sw_long = -77.53091734683608
zoom_value = 2
results = gobnb.Search_all(check_in,check_out,ne_lat,ne_long,sw_lat,sw_long,zoom_value, currency,"")
details_data = []
progress = 1
jsondata = json.dumps(results)
f = open("results.json", "w")
f.write(jsondata)
f.close()
for result in results[:10]:
    data = gobnb.Get_from_room_id(result["room_id"],currency,"")
    details_data.append(data)
    print("len results: ",progress, len(results))
    progress=progress+1
    
details_data_json = json.dumps(details_data)
f = open("details_data.json", "w")
f.write(details_data_json)
f.close()
```

```Python
import gobnb
import json
room_url="https://www.airbnb.com/rooms/[room_id]"
currency="USD"
data = gobnb.Get_from_room_url(room_url,currency,"")
jsondata = json.dumps(data)
f = open("details.json", "w")
f.write(jsondata)
f.close()
```

```Python
import gobnb
import json
room_id=0#obviously the room id
currency="MXN"
data = gobnb.Get_from_room_id(room_id,currency,"")
jsondata = json.dumps(data)
f = open("details.json", "w")
f.write(jsondata)
f.close()
```

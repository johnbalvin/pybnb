# Airbnb scraper in Python

## Overview
This project is an open-source tool developed in Python for extracting product information from Airbnb. It's designed to be easy to use, making it an ideal solution for developers looking for Airbnb product data.

## Features
- Full search support
- Extracts detailed product information from Airbnb
- Implemented in Python just because it's popular
- Easy to integrate with existing Python projects
- The code is optimize to work on this format: ```https://www.airbnb.com/rooms/[roomID]```

## Important
- With the new airbnb changes, if you want to get the price from a room url you need to specify the date range
the date range is should be on the format year-month-day, if you leave the date range empty, you will get the details but not the price


### Install

```bash
$ pip install gobnb
```
## Examples

```Python
import gobnb
import json
currency="MXN"
check_in = "2024-11-02"
check_out = "2024-11-10"
ne_lat = -1.03866277790021
ne_long = -77.53091734683608
sw_lat = -1.1225978433925647
sw_long = -77.59713412765507
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

### example for getting details and price
### if you want to get the price you need to send the check in and check out date
```Python
import gobnb
import json
room_url="https://www.airbnb.com/rooms/30931885"
currency="USD"
check_in = "2024-11-02"
check_out = "2024-11-10"
data = gobnb.Get_from_room_url(room_url,currency,check_in,check_out,"")
jsondata = json.dumps(data)
f = open("details.json", "w")
f.write(jsondata)
f.close()
```

### example for getting details and NOT price
### if you won't want the price, you can just leave it empty
```Python
import gobnb
import json
room_url="https://www.airbnb.com/rooms/33744149"
currency="USD"
check_in = ""
check_out = ""
data = gobnb.Get_from_room_url(room_url,currency,check_in,check_out,"")
jsondata = json.dumps(data)
f = open("details.json", "w")
f.write(jsondata)
f.close()
```

```Python
import gobnb
import json
room_id=18039593#obviously the room id
currency="MXN"
check_in = ""
check_out = ""
data = gobnb.Get_from_room_id(room_id,currency,check_in,check_out,"")
jsondata = json.dumps(data)
f = open("details.json", "w")
f.write(jsondata)
f.close()
```

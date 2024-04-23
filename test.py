import ./src/gobnb
import json

test2()

def test1():
    room_id=668146487515150072
    currency="MXN"
    data = gobnb.Get_from_room_id(room_id,currency,"")
    jsondata = json.dumps(data)
    f = open("details.json", "w")
    f.write(jsondata)
    f.close()


def test2():
    currency="MXN"
    check_in = "2024-05-01"
    check_out = "2024-05-03"
    ne_lat = -1.1225978433925647
    ne_long = -77.59713412765507
    sw_lat = -1.03866277790021
    sw_long = -77.53091734683608
    zoom_value = 2
    results = gobnb.Search_all(check_in,check_out,ne_lat,ne_long,sw_lat,sw_long,zoom_value, currency,"")
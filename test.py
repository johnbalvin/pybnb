import gobnb
import json

def test0():
    room_id=668146487515150072
    currency="MXN"
    check_in = "2024-11-02"
    check_out = "2024-11-10"
    data = gobnb.Get_from_room_id(room_id,currency,check_in,check_out,"")
    jsondata = json.dumps(data)
    f = open("details.json", "w")
    f.write(jsondata)
    f.close()

def test1():
    room_id=668146487515150072
    currency="MXN"
    check_in = "2024-11-02"
    check_out = "2024-11-10"
    data = gobnb.Get_from_room_id(room_id,currency,check_in,check_out,"")
    jsondata = json.dumps(data)
    f = open("details.json", "w")
    f.write(jsondata)
    f.close()


def test2():
    currency="MXN"
    check_in = "2024-11-02"
    check_out = "2024-11-10"
    ne_lat = -1.03866277790021
    ne_long = -77.53091734683608
    sw_lat = -1.1225978433925647
    sw_long = -77.59713412765507
    zoom_value = 2
    results = gobnb.Search_all(check_in,check_out,ne_lat,ne_long,sw_lat,sw_long,zoom_value, currency,"")
    jsondata = json.dumps(results)
    f = open("search.json", "w")
    f.write(jsondata)
    f.close()
    
test1()

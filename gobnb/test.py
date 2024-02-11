from details import *
from search import *
#"%s-%s-%s", year, month, day)
roomURL="https://www.airbnb.com/rooms/668146487515150072"
currency="MXN"
check_in = "2024-02-11"
check_out = "2024-02-14"
ne_lat = -1.1225978433925647
ne_long = -77.59713412765507
sw_lat = -1.03866277790021
sw_long = -77.53091734683608
zoom_value = 2
results = Search_all(check_in,check_out,ne_lat,ne_long,sw_lat,sw_long,zoom_value,"", currency,"")
details_data = []
progress = 1
jsondata = json.dumps(results)
f = open("results.json", "w")
f.write(jsondata)
f.close()
for result in results[:10]:
    data = Get_from_room_id(result["room_id"],currency,"")
    details_data.append(data)
    print("len results: ",progress, len(results))
    progress=progress+1



details_data_json = json.dumps(details_data)
f = open("details_data.json", "w")
f.write(details_data_json)
f.close()

#print("jsondata: ",jsondata)
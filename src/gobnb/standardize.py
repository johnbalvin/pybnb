import re
from gobnb.utils import get_nested_value,parse_price_symbol

regex_number =  re.compile(r'\d+')
            
def standardize_search(results):
    datas = []
    for result in results:
        type_name = get_nested_value(result,"__typename","")
        if type_name!="StaySearchResult":
            continue
        lt = get_nested_value(result,"listing",{})
        pr = get_nested_value(result,"pricingQuote.structuredStayDisplayPrice",{})
        data = {
            "room_id":  int(lt["id"]),
            "category": get_nested_value(lt,"roomTypeCategory",""),
            "kind":     get_nested_value(lt,"pdpUrlType",""),
            "name":     get_nested_value(lt,"name",""),
            "title":    get_nested_value(lt,"title",""),
            "type":     get_nested_value(lt,"listingObjType",""),
            "long_stay_discount":{},
            "fee":{
                "airbnb":{},
                "cleaning":{},
            },
            "price": {
                "unit":{
                    "qualifier":  get_nested_value(pr,"primaryLine.qualifier","") 
                },
                "total":{},
                "break_down":[],
            },
            "rating":{
                "value":0,
                "reviewCount": 0,
            },
            "images": [],
            "badges": [],
            "coordinates":{
                "latitude": get_nested_value(lt,"coordinate.latitude",0),
                "longitud": get_nested_value(lt,"coordinate.longitude",0),
            },
        }
        for badge in get_nested_value(lt,"formattedBadges",[]):
            data["badges"].append(get_nested_value(badge,"loggingContext.badgeType",""))

        avgRatingLocalized = get_nested_value(lt,"avgRatingLocalized","")
        splited = avgRatingLocalized.split(" ")
        if len(splited)==2:
            rating = float(splited[0])
            data["rating"]["value"]=rating
            reviewCount = regex_number.search(splited[1]).group()
            data["rating"]["reviewCount"]=reviewCount
        price_to_use = get_nested_value(pr,"primaryLine.originalPrice","")
        if price_to_use=="":
              price_to_use = get_nested_value(pr,"primaryLine.price","")

        if price_to_use!="": 
            amount, currency = parse_price_symbol(price_to_use)
            data["price"]["unit"]["curency_symbol"]=currency
            data["price"]["unit"]["amount"]=amount   

        discountedPrice=get_nested_value(pr,"primaryLine.discountedPrice","")
        if discountedPrice!="":
            amount, _ = parse_price_symbol(discountedPrice)
            data["price"]["unit"]["discount"]=amount

        splited = get_nested_value(pr,"secondaryLine.price","").split(" ")
        price_to_use=""
        match len(splited):
            case 2:
                price_to_use=splited[0]
            case 3:
                splited = splited[:len(splited)-1]
                price_to_use = "".join(splited)
            case _:
                print("error check: ",splited )
                continue

        amount, currency = parse_price_symbol(price_to_use)
        data["price"]["total"]["currency_symbol"]=currency
        data["price"]["total"]["amount"]=amount
        for image_data in get_nested_value(lt,"contextualPictures",[]):
            img={"url": get_nested_value(image_data,"picture","")}
            data["images"].append(img)   
        for price_detail in get_nested_value(pr,"explanationData.priceDetails",[]):
            if "items" not in price_detail:
                continue
            for item in get_nested_value(price_detail,"items",[]): 
                amount, currency = parse_price_symbol(item["priceString"])
                data["price"]["break_down"].append({"description":item["description"],"amount":amount,"currency":currency})
                match item["displayComponentType"]:
                    case "DISCOUNTED_EXPLANATION_LINE_ITEM":
                        match item["description"]:
                            case "Long stay discount":
                                data["long_stay_discount"]["amount"]=amount
                                data["long_stay_discount"]["currency_symbol"]=currency
                    case "DEFAULT_EXPLANATION_LINE_ITEM":
                        match item["description"]:
                            case "Cleaning fee":
                                data["fee"]["cleaning"]["amount"]=amount
                                data["fee"]["cleaning"]["currency_symbol"]=currency
                            case "Airbnb service fee":
                                data["fee"]["airbnb"]["amount"]=amount
                                data["fee"]["airbnb"]["currency_symbol"]=currency
        datas.append(data)

    return datas
        

def standardize_details(meta):
    ev = meta["data"]["presentation"]["stayProductDetailPage"]["sections"]["metadata"]["loggingContext"]["eventDataLogging"]
    data = {
        "coordinates": {
                "latitude":         get_nested_value(ev,"listingLat",0),
                "longitude":        get_nested_value(ev,"listingLng",0),
        },
        "room_type":                get_nested_value(ev,"roomType",""),
        "is_super_host":            get_nested_value(ev,"isSuperhost",""),
        "home_tier":                get_nested_value(ev,"homeTier",""),
        "person_capacity":          get_nested_value(ev,"personCapacity",0),
        "rating":{
            "accuracy":             get_nested_value(ev,"accuracyRating",0),
            "checking":             get_nested_value(ev,"checkinRating",0),
            "cleanliness":          get_nested_value(ev,"cleanlinessRating",0),
            "communication":        get_nested_value(ev,"communicationRating",0),
            "location":             get_nested_value(ev,"locationRating",0),
            "value":                get_nested_value(ev,"valueRating",0),
            "guest_satisfaction":   get_nested_value(ev,"guestSatisfactionOverall",0),
            "review_count":         get_nested_value(ev,"visibleReviewCount",0),
        },
        "house_rules":{
            "aditional":"",
            "general": [],
        },
        "host":{
                "id":"",   
                "name":"",  
                "joined_on":"",  
                "description":"",  
        },
        "sub_description":{
            "title":"",
            "items": [],
        },
        "amenities": [],
        "co_hosts":[],
        "images":[],
        "location_descriptions":[],
        "highlights":[],
    }

    sd = get_nested_value(meta,"data.presentation.stayProductDetailPage.sections.sbuiData")
    for section in get_nested_value(sd,"sectionConfiguration.root.sections",[]):
        typeName=get_nested_value(section,"sectionData.__typename","")
        if typeName == "PdpHostOverviewDefaultSection":
            data["host"]={
                "id" :  get_nested_value(section,"sectionData.hostAvatar.loggingEventData.eventData.pdpContext.hostId",""),
                "name": get_nested_value(section,"sectionData.title",""),
            }
        elif typeName == "PdpOverviewV2Section":
            data["sub_description"]["title"]=get_nested_value(section,"sectionData.title","")
            for item in get_nested_value(section,"sectionData.overviewItems",[]):
                data["sub_description"]["items"].append(get_nested_value(item,"title",""))

    for section in get_nested_value(meta,"data.presentation.stayProductDetailPage.sections.sections",[]):
        typeName=get_nested_value(section,"section.__typename","")
        match typeName:
            case "HostProfileSection": 
                data["host"]["id"] = get_nested_value(section,"section.hostAvatar.userID","")
                data["host"]["name"] = get_nested_value(section,"section.title","")
                data["host"]["joined_on"] = get_nested_value(section,"section.subtitle","")
                data["host"]["description"] = get_nested_value(section,"section.hostProfileDescription.htmlText","")
                for cohost in get_nested_value(section,"section.additionalHosts",[]):
                    data["co_hosts"].append({"id":cohost.get("id",""),"name":cohost.get("name","")})
            case "PhotoTourModalSection":  
                for mediaItem in get_nested_value(section,"section.mediaItems",[]):
                    img={
                        "title": mediaItem.get("accessibilityLabel",""),
                        "url": mediaItem.get("baseUrl",""),
                    }
                    data["images"].append(img)
            case "PoliciesSection":        
                for houseRulesSection in get_nested_value(section,"section.houseRulesSections",[]):
                    house_rule={
                        "title": houseRulesSection.get("title",""),
                        "values":[],
                    }
                    for item in houseRulesSection.get("items",[]):
                            if item.get("title","")=="Additional rules":
                                data["house_rules"]["aditional"]=get_nested_value(item,"html.htmlText","")
                                continue
                            house_rule["values"].append({"title":item.get("title","") ,"icon": item.get("icon","")})

                    data["house_rules"]["general"].append(house_rule)
            case "LocationSection":
                for locationDetail in get_nested_value(section,"section.seeAllLocationDetails",[]):
                    seeAllLocationDetail={
                        "title": locationDetail.get("title",""),
                        "content": get_nested_value(locationDetail,"content.htmlText"),
                    }
                    data["location_descriptions"].append(seeAllLocationDetail)
            case "PdpTitleSection":           
                    data["title"]=section.get("title","")
            case "PdpHighlightsSection":
                for highlitingData in get_nested_value(section,"section.highlights",[]):
                    highliting={
                        "title": highlitingData.get("title",""),
                        "subtitle": highlitingData.get("subtitle",""),
                        "icon": highlitingData.get("icon",""),
                    }
                    data["highlights"].append(highliting)
            case "PdpDescriptionSection":
                data["description"]=  get_nested_value(section,"section.htmlDescription.htmlText","")
            case "AmenitiesSection":  
                for amenityGroupRaw in get_nested_value(section,"section.seeAllAmenitiesGroups",[]):
                    amenityGroup={
                        "title": amenityGroupRaw.get("title",""),
                        "values": [],
                    }
                    for amenityRaw in amenityGroupRaw.get("amenities",[]):
                        amenity = {
                            "title":     amenityRaw.get("title",""),
                            "subtitle":  amenityRaw.get("subtitle",""),
                            "icon":      amenityRaw.get("icon",""),
                            "available": amenityRaw.get("available",""),
                        }
                        amenityGroup["values"].append(amenity)
                    data["amenities"].append(amenityGroup)
    return data


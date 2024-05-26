import gobnb.api as api
from datetime import datetime
from urllib.parse import urlencode
from gobnb.standardize import get_nested_value,standardize_search
from curl_cffi import requests

treament = [
	"feed_map_decouple_m11_treatment",
	"stays_search_rehydration_treatment_desktop",
	"stays_search_rehydration_treatment_moweb",
	"selective_query_feed_map_homepage_desktop_treatment",
	"selective_query_feed_map_homepage_moweb_treatment",
]

def Search_all(check_in:str, check_out:str, ne_lat:float, ne_long:float, sw_lat:float, sw_long:float, zoom_value:int, currency:str, proxy_url:str):
    api_key = api.get(proxy_url)
    all_results = []
    cursor = ""
    while True:
        results_raw = search(check_in,check_out,ne_lat,ne_long,sw_lat,sw_long,zoom_value,cursor, currency, api_key, proxy_url)
        results = standardize_search(results_raw.get("searchResults",[]))
        all_results = all_results + results
        if len(results)==0 or "nextPageCursor" not in results_raw["paginationInfo"] or  results_raw["paginationInfo"]["nextPageCursor"] is None:
            break
        cursor = results_raw["paginationInfo"]["nextPageCursor"]
    return all_results

def Search_first_page(check_in:str, check_out:str, ne_lat:float, ne_long:float, sw_lat:float, sw_long:float, zoom_value:int, cursor:str, currency:str, proxy_url:str):
    api_key = api.get(proxy_url)
    results = search(check_in,check_out,ne_lat,ne_long,sw_lat,sw_long,zoom_value,"", currency, api_key, proxy_url)
    results = standardize_search(results)
    return results

def search(check_in:str, check_out:str, ne_lat:float, ne_long:float, sw_lat:float, sw_long:float, zoom_value:int, cursor:str, currency:str, api_key:str, proxy_url:str):
    check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
    check_out_date = datetime.strptime(check_out, "%Y-%m-%d")

    difference = check_out_date - check_in_date

    days = difference.days

    base_url = "https://www.airbnb.com/api/v3/StaysSearch/d4d9503616dc72ab220ed8dcf17f166816dccb2593e7b4625c91c3fce3a3b3d6"
    query_params = {
        "operationName": "StaysSearch",
        "locale": "en",
        "currency": currency,
    }
    url_parsed = f"{base_url}?{urlencode(query_params)}"
    rawParams=[
        {"filterName":"cdnCacheSafe","filterValues":["false"]},
        {"filterName":"channel","filterValues":["EXPLORE"]},
        {"filterName":"checkin","filterValues":[check_in]},
        {"filterName":"checkout","filterValues":[check_out]},
        {"filterName":"datePickerType","filterValues":["calendar"]},
        {"filterName":"flexibleTripLengths","filterValues":["one_week"]},
        {"filterName":"itemsPerGrid","filterValues":["50"]},#if you read this, this is items returned number, this can bex exploited  ;)
        {"filterName":"monthlyLength","filterValues":["3"]},
        {"filterName":"monthlyStartDate","filterValues":["2024-02-01"]},
        {"filterName":"neLat","filterValues":[str(ne_lat)]},
        {"filterName":"neLng","filterValues":[str(ne_long)]},
        {"filterName":"placeId","filterValues":["ChIJpTeBx6wjq5oROJeXkPCSSSo"]},
        {"filterName":"priceFilterInputType","filterValues":["0"]},
        {"filterName":"priceFilterNumNights","filterValues":[str(days)]},
        {"filterName":"query","filterValues":["Galapagos Island, Ecuador"]},
        {"filterName":"screenSize","filterValues":["large"]},
        {"filterName":"refinementPaths","filterValues":["/homes"]},
        {"filterName":"searchByMap","filterValues":["true"]},
        {"filterName":"swLat","filterValues":[str(sw_lat)]},
        {"filterName":"swLng","filterValues":[str(sw_long)]},
        {"filterName":"tabId","filterValues":["home_tab"]},
        {"filterName":"version","filterValues":["1.8.3"]},
        {"filterName":"zoomLevel","filterValues":[str(zoom_value)]},
    ]
    inputData = {
        "operationName":"StaysSearch",
        "extensions":{
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "d4d9503616dc72ab220ed8dcf17f166816dccb2593e7b4625c91c3fce3a3b3d6",
            },
        },
        "variables":{
            "includeMapResults": True,
            "isLeanTreatment": False,
            "staysMapSearchRequestV2": {
                "cursor":cursor,
                "requestedPageType":"STAYS_SEARCH",
                "metadataOnly":False,
                "source":"structured_search_input_header",
                "searchType":"user_map_move",
                "treatmentFlags":treament,
                "rawParams":rawParams,
            },
            "staysSearchRequest": {
                "cursor":cursor,
                "maxMapItems": 9999,
                "requestedPageType":"STAYS_SEARCH",
                "metadataOnly":False,
                "source":"structured_search_input_header",
                "searchType":"user_map_move",
                "treatmentFlags":treament,
                "rawParams":rawParams,
            },
        },
    }
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en",
        "Cache-Control": "no-cache",
        "Connection": "close",
        "Pragma": "no-cache",
        "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "Sec-Ch-Ua-Mobile": "?0",
        "X-Airbnb-Api-Key": api_key,
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    proxies = {}
    if proxy_url:
        parsed_proxy_url = requests.utils.requote_uri(proxy_url)
        proxies = {"http": parsed_proxy_url, "https": parsed_proxy_url}
    response = requests.post(url_parsed, json = inputData, headers=headers, proxies=proxies,  impersonate="chrome110")
    data = response.json()
    to_return=get_nested_value(data,"data.presentation.staysSearch.results",{})
    return to_return

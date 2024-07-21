from curl_cffi import requests
from gobnb.parse import parse_body_details_wrapper
from gobnb.price import get_price

def Get_from_room_url(roomURL: str, currency: str, check_in: str, check_out: str, proxy_url: str):
    data, price_input, cookies = get_from_room_url(roomURL, proxy_url)
    if check_in is None or check_in == "" or check_out is None or check_out == "":
        return data
    dataFullPrice = get_price(price_input["product_id"],price_input["impression_id"],price_input["api_key"],currency, cookies, check_in, check_out, proxy_url)
    data["price"] = dataFullPrice
    return data
def Get_from_room_id(room_id: int, currency: str, check_in: str, check_out: str, proxy_url: str):
    room_url = f"https://www.airbnb.com/rooms/{room_id}"
    data, price_input, cookies = get_from_room_url(room_url, proxy_url)
    if check_in is None or check_in == "" or check_out is None or check_out == "":
        return data
    dataFullPrice = get_price(price_input["product_id"],price_input["impression_id"],price_input["api_key"],currency, cookies, check_in, check_out, proxy_url)
    data["price"] = dataFullPrice
    return data

def Get_from_room_id_and_domain(room_id: int, domain: str, currency: str, check_in: str, check_out: str, proxy_url: str):
    room_url = f"https://{domain}/rooms/{room_id}"
    data, price_input, cookies = get_from_room_url(room_url, proxy_url)
    if check_in is None or check_in == "" or check_out is None or check_out == "":
        return data
    dataFullPrice = get_price(price_input["product_id"],price_input["impression_id"],price_input["api_key"],currency, cookies, check_in, check_out, proxy_url)
    data["price"] = dataFullPrice
    return data

def Get_price_by_url(roomURL: str, currency: str, check_in: str, check_out: str, proxy_url: str):
    data, price_input, cookies = get_from_room_url(roomURL, proxy_url)
    dataFullPrice = get_price(price_input["product_id"],price_input["impression_id"],price_input["api_key"],currency, cookies, check_in, check_out, proxy_url)
    data["price"] = dataFullPrice
    return data

def get_from_room_url(room_url: str, proxy_url: str):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "Sec-Ch-Ua-Mobile": "?0",
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
    response = requests.get(room_url, headers=headers, proxies=proxies)
    response.raise_for_status()
    data_formatted, price_dependency_input=parse_body_details_wrapper(response.text)
    cookies = response.cookies
    return data_formatted, price_dependency_input, cookies
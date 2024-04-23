import json
from curl_cffi import requests
from gobnb.utils import get_nested_value,remove_space,parse_price_symbol
from urllib.parse import urlencode

ep = "https://www.airbnb.com/api/v3/StaysPdpSections"

def get_price(product_id: str,impresion_id: str,api_key: str, currency: str, cookies: list, proxy_url: str) -> (float,str,str):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-Airbnb-Api-Key": api_key,
        }
        entension={
            "persistedQuery": {
                "version":1,
                "sha256Hash": "e6a7821cf0f78dfc0baab6fd111027eb2976355f2aecbb84bc2086ee6e57161b",
            },
        }
        dataRawExtension = json.dumps(entension)
        variablesData={
            "id": product_id,
            "pdpSectionsRequest": {
                "adults": "1",
                "bypassTargetings": None,
                "bypassTargetings":              False,
                "categoryTag":                   None,
                "causeId":                       None,
                "children":                      None,
                "disasterId":                    None,
                "discountedGuestFeeVersion":     None,
                "displayExtensions":             None,
                "federatedSearchId":             None,
                "forceBoostPriorityMessageType": None,
                "infants":                       None,
                "interactionType":               None,
                "layouts":                       ["SIDEBAR", "SINGLE_COLUMN"],
                "pets":                          0,
                "pdpTypeOverride":               None,
                "photoId":                       None,
                "preview":                       False,
                "previousStateCheckIn":          None,
                "previousStateCheckOut":         None,
                "priceDropSource":               None,
                "privateBooking":                False,
                "promotionUuid":                 None,
                "relaxedAmenityIds":             None,
                "searchId":                      None,
                "selectedCancellationPolicyId":  None,
                "selectedRatePlanId":            None,
                "splitStays":                    None,
                "staysBookingMigrationEnabled":  False,
                "translateUgc":                  None,
                "useNewSectionWrapperApi":       False,
                "sectionIds": [
                    "CANCELLATION_POLICY_PICKER_MODAL", "BOOK_IT_CALENDAR_SHEET", "POLICIES_DEFAULT", "BOOK_IT_SIDEBAR", "URGENCY_COMMITMENT_SIDEBAR",
                    "BOOK_IT_NAV", "BOOK_IT_FLOATING_FOOTER", "EDUCATION_FOOTER_BANNER", "URGENCY_COMMITMENT", "EDUCATION_FOOTER_BANNER_MODAL"],
                "checkIn":        None,
                "checkOut":       None,
                "p3ImpressionId": impresion_id,
            },
        }
        dataRawVariables = json.dumps(variablesData)
        query = {
            "operationName": "StaysPdpSections",
            "locale": "en",
            "currency": currency,
            "variables": dataRawVariables,
            "extensions": dataRawExtension,
        }
        url = f"{ep}?{urlencode(query)}"
        
        session = requests.Session()
        if proxy_url:
            session.proxies.update({'http': proxy_url, 'https': proxy_url})

        for name in cookies:
            session.cookies.set(name, cookies[name])

        response = session.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        for section in get_nested_value(data,"data.presentation.stayProductDetailPage.sections.sections",[]):
            if get_nested_value(section,"section.__typename","")=="BookItSection":
                pr=get_nested_value(section,"section.structuredDisplayPrice.primaryLine",{})
                price=remove_space(pr.get("price",""))
                qualifier=remove_space(pr.get("qualifier",""))
                ammount, currency = parse_price_symbol(price)
                return ammount, currency,qualifier
        return 0,"",""
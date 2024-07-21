import json
from curl_cffi import requests
from gobnb.utils import get_nested_value,remove_space,parse_price_symbol
from urllib.parse import urlencode

ep = "https://www.airbnb.com/api/v3/StaysPdpSections/80c7889b4b0027d99ffea830f6c0d4911a6e863a957cbe1044823f0fc746bf1f"

def get_price(product_id: str, impresion_id: str,api_key: str, currency: str, cookies: list, checkIn: str, checkOut: str, proxy_url: str) -> (str):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-Airbnb-Api-Key": api_key,
        }
        entension={
            "persistedQuery": {
                "version":1,
                "sha256Hash": "80c7889b4b0027d99ffea830f6c0d4911a6e863a957cbe1044823f0fc746bf1f",
            },
        }
        dataRawExtension = json.dumps(entension)
        variablesData={
            "id": product_id,
            "pdpSectionsRequest": {
                "adults": "1",
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
                "sectionIds": ["BOOK_IT_FLOATING_FOOTER","POLICIES_DEFAULT","EDUCATION_FOOTER_BANNER_MODAL",
                        "BOOK_IT_SIDEBAR","URGENCY_COMMITMENT_SIDEBAR","BOOK_IT_NAV","MESSAGE_BANNER","HIGHLIGHTS_DEFAULT",
                        "EDUCATION_FOOTER_BANNER","URGENCY_COMMITMENT","BOOK_IT_CALENDAR_SHEET","CANCELLATION_POLICY_PICKER_MODAL"],
                "checkIn":        checkIn,
                "checkOut":       checkOut,
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

        sections = get_nested_value(data,"data.presentation.stayProductDetailPage.sections.sections",{})
        for section in sections:
            if section['sectionId'] == "BOOK_IT_SIDEBAR":
                price_data = get_nested_value(section,"section.structuredDisplayPrice",{})
                finalData={
                     "main":{
                        "price":get_nested_value(price_data,"primaryLine.price",{}),
                        "discountedPrice":get_nested_value(price_data,"primaryLine.discountedPrice",{}),
                        "originalPrice":get_nested_value(price_data,"primaryLine.originalPrice",{}),
                        "qualifier":get_nested_value(price_data,"primaryLine.qualifier",{}),
                     },
                     "details":{},
                }
                details = get_nested_value(price_data,"explanationData.priceDetails",{})
                for detail in details:
                    for item in get_nested_value(detail,"items",{}):
                         finalData["details"][item["description"]]=item["priceString"]
                return finalData
        return {}
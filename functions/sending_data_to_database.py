import time
import datetime
import itertools

import googlemaps
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin
cred = credentials.Certificate('functions/appproject-9a187-firebase-adminsdk-nt2jm-49d382129b.json')
firebase_admin.initialize_app(cred)
# firebase_admin.initialize_app()
db = firestore.client()


def check_five_combinations(string: str) -> bool:
    """checks if string contains all 5 unicode characters

    Args:
        string (string): string to check

    Returns:
        boolean: True if string contains all 5 unicode characters. else False
    """
    unicode_chars = ["ⓚ", "ⓝ", "ⓢ", "ⓣ", "ⓐ"]
    for i in range(1, len(unicode_chars) + 1):
        for combination in itertools.combinations(unicode_chars, i):
            if ''.join(combination) in string:
                return True
    return False


# def geocode_address(address):
#     """Use Google Maps Geocoding API to convert address to coordinates
#     Keyword arguments:
#     argument -- description
#     Return: return_description
#     """
#     # response = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key=", timeout=5)
#     # resp_json = response.json()
#
#     # if resp_json['status'] == 'OK':
#     #     latitude = resp_json['results'][0]['geometry']['location']['lat']
#     #     longitude = resp_json['results'][0]['geometry']['location']['lng']
#     #     return latitude, longitude
#     # else:
#     #     print(resp_json)
#     #     exit(1)
#     #     # return None, None
#
#     gmaps = googlemaps.Client(key='')
#     geocode_result = gmaps.geocode(address)
#     print(geocode_result)
#     if geocode_result:
#         latitude = geocode_result[0]['geometry']['location']['lat']
#         longitude = geocode_result[0]['geometry']['location']['lng']
#         return latitude, longitude
#     else:
#         print(geocode_result)
#         exit(1)


def add_store_to_firestore(store_data):
    # Assume store_data is a dictionary with necessary fields
    db.collection('stores').add(store_data)


def get_datas_from_firestore():
    # Example: Getting existing store addresses from Firestore
    datas = []
    stores = db.collection('stores').get()
    for store in stores:
        datas.append(store.to_dict()['storeAddress'])

        print(f'{store.id} => {store.to_dict()}')

    return datas


_from_db = get_datas_from_firestore()

print(f"\n\n{_from_db}\n\n")

stores = []
# Example: Loading store data (could be from a file)
with open('functions/osupumplist2/testrun.txt', 'r', encoding='utf-8') as f:
    data = f.read().split('\n')
    it = iter(data)
    for f in it:
        print(f)
        if f.startswith('#'):
            continue
        if f in _from_db:
            print("DUPLICATE FOUND")
            continue

        req = {
            # "storeName": "",
            # "address": "",
            # # 'coords': {'lat': 30.21341324, 'lng': 12.2581274},
            # "storeSupport": "ⓚⓝⓢⓣⓐ",
            # storeInfo : "갸아아악”
            # storeHours : "영업시간”
            # time : "등록/수정 시간”
        }

        last = f.split()[-1]
        # parse storeName
        print(f.split()[-1])
        if check_five_combinations(last):
            req.update({"storeName": "".join(f.split()[1:-1])})
        else:
            req.update({"storeName": "".join(f.split()[1:])})

        # parse storeSupport
        
        if check_five_combinations(last):
            req.update({"storeSupport": last})
        else:
            req.update({"storeSupport": "N\\A"})

        # parse storeAddress
        req.update({"storeAddress": next(it)})

        if req['storeAddress'] in _from_db:
            print("NAME NOT DUPLICATE, BUT DUPLICATE ADDRESS FOUND. SKIPPING")
            continue

        # # geocode storeAddress
        # time.sleep(1)
        # lat, lng = geocode_address(req['storeAddress'])
        # req.update({'coords': {'lat': lat, 'lng': lng}})

        # add dummy storeInfo
        req.update({"storeInfo": ""})

        # add dummy storeHours
        req.update({"storeHours": ""})

        # add time created
        # format to YYYY-MM-DD HH:MM:SS
        req.update({"createdAt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

        # print(req)

        stores.append(req)

        # Example: Adding store data to Firestore
        add_store_to_firestore(req)


print(stores)

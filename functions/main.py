# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn, firestore_fn
from firebase_admin import initialize_app, firestore

# from dotenv import load_dotenv
import googlemaps

import math


# load_dotenv()
initialize_app()

_API_KEY = "AIzaSyB69E5-_NFjy7FJZPyaRzzsKZGHju3jVe8" # this is ok because it's a public API key and it's restricted to google maps related APIs
# _API_KEY = os.getenv("G")
gmap = googlemaps.Client(_API_KEY)


# @https_fn.on_request()
# def on_request_example(req: https_fn.Request) -> https_fn.Response:
#     return https_fn.Response("Hello world!")


@firestore_fn.on_document_created(document="stores/{storeId}", region="asia-northeast2")
def on_document_created_example(
    event: firestore_fn.Event[firestore_fn.DocumentSnapshot | None]
) -> None:
    """Triggered when a document is created. automatically geocodes the address and adds it to 'coords' field"""
    doc_id = event.id
    print(f"Created document: {doc_id}")

    doc = event.data.to_dict()

    address = doc.get("storeAddress")

    if address:
        geocode_result = gmap.geocode(address)
        if geocode_result:
            coords = geocode_result[0]["geometry"]["location"]
            event.data.reference.update({"coords": coords})
            print(f"Updated document: {doc_id}")
        else:
            print(f"Could not geocode address: {address}")
    else:
        print(f"Document {doc_id} has no storeAddress field")


# @firestore_fn.on_document_updated()
# def on_document_updated_example(
#     event: firestore_fn.Event
# ) -> None:
#     """Triggered when a document is updated. automatically geocodes the address and adds it to 'coords' field"""


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great circle distance between two points on the earth (specified in decimal degrees)"""
    # https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points 등...

    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    r = 6371 # Radius of earth in kilometers.
    return c * r

# firebase는 geoquery를 지원하지 않는다.
# firebase geofire를 사용하려고 했으나, python용 라이브러리가 없다. 그러면 javascript로 다시 써야 하고, 각 document에 대해 hash를 계산해서 놓아야 한다고 한다.
# 그래서 그냥 firestore에서 store를 가져와서, python으로 계산하는 방법을 사용하려고 한다.


@https_fn.on_request(region="asia-northeast2")
def find_stores_nearby_n_km_radius(
    req: https_fn.CallableRequest
) -> https_fn.Response:
    """Returns a list of stores within a given radius of a given location"""
    # get the location from sent data
    center_lat = req.args.get("lat")
    center_lng = req.args.get("lng")
    R = req.args.get("radius") # meters
    center_lat, center_lng, R = map(float, [center_lat, center_lng, R])

    db = firestore.client()
    stores_ref = db.collection("stores")
    stores = stores_ref.stream() # 제한을 두지 않으면, 모든 store를 가져온다. 이건 좋지 않은 방법이다. 나중에 수정해야 한다.
    # 성능 실험 해야 할듯... (100개 이상의 store가 있으면, 어떻게 되는지)

    # get the stores within the radius
    stores_within_radius = []
    for doc in stores:
        store_data = doc.to_dict()
        store_coords = store_data.get("coords")
        if store_coords and haversine(center_lat, center_lng, store_coords["lat"], store_coords["lng"]) <= R:
            stores_within_radius.append(store_data)
    
    return stores_within_radius

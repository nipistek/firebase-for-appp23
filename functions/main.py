# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn, firestore_fn
from firebase_admin import initialize_app, firestore

# from dotenv import load_dotenv
import googlemaps

import math, os


# load_dotenv()
initialize_app()

_API_KEY = "AIzaSyB69E5-_NFjy7FJZPyaRzzsKZGHju3jVe8" # this is ok because it's a public API key and it's restricted to google maps related APIs
# _API_KEY = os.getenv("G")
gmap = googlemaps.Client(_API_KEY)


@https_fn.on_request()
def on_request_example(req: https_fn.Request) -> https_fn.Response:
    return https_fn.Response("Hello world!")


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


# 아직 완성 안된 메소드 (아래)
# @https_fn.on_request()
# def on_request_calculate_10km_markers(req: https_fn.Request) -> https_fn.Response:
#     """Gets all stores within 10km of the user's location and returns a list of their IDs"""
#     user_coords = req.json.get("coords")
#
#     if not user_coords:
#         return https_fn.Response("No coords provided", status=400)
#
#     stores = firestore.client().collection("stores").stream()
#
#     stores_within_10km = []
#
#     for store in stores:
#         store_coords = store.get("coords")
#         if store_coords:
#             distance = gmap.distance_matrix(user_coords, store_coords)["rows"][0]["elements"][0]["distance"]["value"]
#             if distance <= 10000:
#                 stores_within_10km.append(store.id)
#
#     # or calculate manually with haversine formula
#     # https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
#     # https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
#     # for store in stores:
#     #     store_coords = store.get("coords")
#     #     if store_coords:
#     #         distance = 6371 * math.acos(math.cos(math.radians(user_coords["lat"])) * math.cos(math.radians(store_coords["lat"])) * math.cos(math.radians(store_coords["lng"]) - math.radians(user_coords["lng"])) + math.sin(math.radians(user_coords["lat"])) * math.sin(math.radians(store_coords["lat"])))
#     #         if distance <= 10000:
#     #             stores_within_10km.append(store.id)
#
#     return https_fn.Response(stores_within_10km)
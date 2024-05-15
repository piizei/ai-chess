import os

import pymongo

DB_NAME = "admin"
COLLECTION_NAME = "state"
CONNECTION_STRING = os.environ.get("MONGO_CONNECTION")


def get_collection():
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client[DB_NAME]
    if DB_NAME not in client.list_database_names():
        # Create a database with 400 RU throughput that can be shared across
        # the DB's collections
        db.command({"customAction": "CreateDatabase", "offerThroughput": 400})
        print("Created db '{}' with shared throughput.\n".format(DB_NAME))
    else:
        print("Using database: '{}'.\n".format(DB_NAME))
    collection = db[COLLECTION_NAME]
    if COLLECTION_NAME not in db.list_collection_names():
        # Creates a unsharded collection that uses the DBs shared throughput
        db.command(
            {"customAction": "CreateCollection", "collection": COLLECTION_NAME}
        )
        print("Created collection '{}'.\n".format(COLLECTION_NAME))
    else:
        print("Using collection: '{}'.\n".format(COLLECTION_NAME))
    return collection

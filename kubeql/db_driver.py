from pymongo.database import Database
from pymongo import MongoClient
from pymongo import results


def get_new_db(
    database_name: str, username: str = "root", password: str = "example"
) -> Database:
    return MongoClient(port=27017, username=username, password=password)[database_name]


def clear_collection(db: Database, collection: str) -> results.DeleteResult:
    return db[collection].delete_many({})

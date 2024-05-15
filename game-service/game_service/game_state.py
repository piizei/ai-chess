import datetime

from game_service.mongo_utils import get_collection


def create_game(start_date: datetime.datetime):
    collection = get_collection()
    game = {
        "starts": start_date,
        "is_over": False,
        "winner": None,
        "moves": [],
        "current_fen": "",
        "game_id": "",
    }
    result = collection.insert_one(game)

def check_game():
    collection = get_collection()
    #find games that are started (start date is before datetime.now( and  are not over and have no game_id
    return get_collection().find_one({"starts": {"$lt": datetime.datetime.now()}, "is_over": False, "game_id": ""})

from dotenv import load_dotenv

load_dotenv()
import requests

base_url = "http://localhost:3000/api/v1/chess/two"
stockfish = "http://localhost:8080/"

def test_game():

    # Start a new game
    response = requests.get(f"{base_url}")
    assert response.status_code == 200
    # get the json object
    game_id = response.json()["game_id"]

    game_over = False
    while not game_over:
        # Get the board
        response = requests.post(f"{base_url}/fen", json={"game_id": game_id})
        assert response.status_code == 200
        fen = response.json()["fen_string"]

        # Let the AI make a move
        response = requests.post(stockfish, json={"fen": fen})
        assert response.status_code == 200
        move = response.text.split(" ")[1]
        (start, end) = move[:2], move[2:]
        response = requests.post(f"{base_url}/move", json={"game_id": game_id, "from": start, "to": end})

        # Check if the game is over
        response = requests.post(f"{base_url}/check", json={"game_id": game_id})
        assert response.status_code == 200
        game_over = response.json()["status"] != "game continues"

def test_chess_api_moves_endpoint():
    response = requests.post(stockfish+'/3', json={"fen": '4qr2/p1r3k1/b2p1p1p/2pP2p1/Pp2P3/1P2R2P/2QN1PPK/4R3 w - - 70 113'})
    print(response.text)

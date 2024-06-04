import argparse
from datetime import datetime, timedelta
from game_service.game_state import create_game

# Create the parser
parser = argparse.ArgumentParser(description='Create a new game')

# Add the arguments
parser.add_argument('hours', type=int, help='The number of hours from now when the game will start')

# Parse the arguments
args = parser.parse_args()

# Calculate the game start time
game_start_time = datetime.now() + timedelta(hours=args.hours)

# Create the game
create_game(game_start_time)

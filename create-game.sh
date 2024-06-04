#!/usr/bin/env bash
# This script creates a new game in the database
# It takes number of hours as parameter (integer, from this moment, when the game will start)
# and calls the Python script create_game.py with the number of hours as an argument

# Check if a parameter has been provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <number of hours>"
    exit 1
fi

# Call the Python script with the number of hours as an argument
python3 game_service/create_game.py $1

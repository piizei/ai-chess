# ai-chess
Play chess against LLM.

The projects is assembled from microservices.
Following services are used from GitHub as is, and are not modified:
- Stockfish server https://github.com/hyugit/stockfish-server/ with GPLv3 license)
- chess-api https://github.com/anzemur/chess-api with MIT license

The rest are home-made and with MIT license.
- chess-ui (this is effort of multiple people)
- game-service

## Installation
Easy peasy, azure developer cli: `azd up`
(creates cloud resources, cost will apply)

Destroy the env with `azd down`

![chess-screenshot.png](chess-screenshot.png)

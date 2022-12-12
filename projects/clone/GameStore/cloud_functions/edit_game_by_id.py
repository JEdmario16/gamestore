from pymongo import MongoClient
from bson.json_util import dumps
from json_response_generator import generate_json_response
import json


from flask import Flask, request

import jwt
from jwt.exceptions import (
    InvalidSignatureError,
    InvalidTokenError,
    ExpiredSignatureError,
)

a = Flask(__name__)


@a.route("/edit_game_by_id", methods=["PUT"])
def edit_game_by_id():

    """
    This function edit a game by id. It will be called when
    the endpoint is triggered by a HTTP request.
    This endpoint need authorization by jwt token
    The url is generated by Google Cloud Functions
    api_url = https://us-central1-teste-371002.cloudfunctions.net/edit_game_by_id?

    This endpoint need a id as parameter, this parameter is passed by the url.

    params:
        request: HTTP request object.
        id: Id of the game to be edited (passed by the url)
    returns:
        Json response with the game data

    Notes:
        - if the id is not passed by the url, the function will return a error
        - if the id is not valid, the function will return a error
        - if the id is valid, but the game is not found, the function will return a error
        - if the id is valid, but the game is found, the function will return the game data
    """

    # Verify request jwt signature
    # Get the token from the header

    token = request.headers.get("Authorization", None)
    public_key = open("public_key.pem", "r", encoding="utf-8").read()

    # Check if the token is valid
    try:
        jwt.decode(token, public_key, algorithms=["RS256"])  # type: ignore

    except (
        InvalidSignatureError,
        InvalidTokenError,
        ExpiredSignatureError,
    ) as e:
        return generate_json_response(
            status_code=401,
            message="Invalid token",
            data=e.args,  # type: ignore there is no data to return
            request_params={"token": token},
        )

    # Get the id from the url
    game_id = request.args.get("game_id", None)


    # Get the payload from the request
    try:
        payload = request.get_json()
        data_to_edit = payload["data_to_edit"]
        status = None

        # Get the request params
        request_params = {"game_id": game_id, "data_to_edit": data_to_edit}
    
    except Exception as e:
        return generate_json_response(
            status_code=400,
            message="No json data was passed or invalid json data",
            data=e.args,  # type: ignore there is no data to return
            request_params={"game_id": game_id, "data_to_edit": []},
        )	

    # Check if the id is valid
    try:
        game_id = int(game_id) if game_id else None

    except ValueError:
        return generate_json_response(
            status_code=400,
            message="Invalid game id",
            data=None,  # type: ignore there is no data to return
            request_params={
                "game_id": game_id,
                "request_params": request_params,
            },
        )

    # Connect to the database
    client = MongoClient(
        "mongodb+srv://root:1234@cluster0.gg84ero.mongodb.net/?retryWrites=true&w=majority"
    )

    db = client["Catalog"]
    collection = db["games"]

    # Check if the game is found. It is not mandatory, but mongoDB not return any error if the game is not found
    # So, I check if the game is found, if not, return a error
    game = collection.find_one({"game_id": game_id})

    if not game:
        return generate_json_response(
            status_code=404,
            message="Game not found",
            data=None,  # type: ignore
            request_params=request_params,
        )

    # edit the game, and check if the game was edited
    res = collection.update_one({"game_id": game_id}, {"$set": data_to_edit})
    status = bool(res.modified_count)

    # Generate the response

    if status:
        return generate_json_response(
            status_code=200,
            message="Game edited successfully",
            data=data_to_edit,  # type: ignore because the data is a dict
            request_params=request_params,
        )

    return generate_json_response(
        status_code=404,
        message="No changes were made",
        data=None,  # type: ignore there is no data to return
        request_params=request_params,
    )


if __name__ == "__main__":
    a.run(debug=True, port=8080)
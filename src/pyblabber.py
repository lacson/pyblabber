"""
    pyblabber.py
    Jonathan Lacson
    CS 2304 Spring 2019

    Contains main entrypoint for pyblabber.
    Hosts hello world test page at /.
"""
from flask import Flask, make_response, request, render_template
from pymongo import MongoClient
from os import getenv
import json
import uuid
import time

# create Flask instance
flaskApp = Flask(__name__, template_folder="resources")

# connect to mongo server
mongo = MongoClient('mongo', 27017)

# make blabs callable
blabDB = mongo["blabs"]
blabCollection = blabDB["blabs"]

# host our hello world html page
@flaskApp.route('/')
def home():
    """
    Responds to root on default port

    :return: served hello world web page
    """
    return render_template("hello_world.html")

# POST method to add a new blab
@flaskApp.route('/blabs', methods = ['POST'])
def addBlab():
    """
    Handles POST request to add a blab.

    :return: 201 and (json) Appropriate response as defined in Blabber specs,
             400 if request schema was not valid.
    """
    # get our request data
    reqBody = request.get_json(force = True)

    # verify that we got valid inputs
    try:
        reqBody["author"]
    except KeyError:
        return make_response(json.dumps({"error": True, "message": "An author is required."}), 400)

    try:
        reqBody["author"]["email"]
    except KeyError:
        return make_response(json.dumps({"error": True, "message": "An email is required."}), 400)

    try:
        reqBody["author"]["name"]
    except KeyError:
        return make_response(json.dumps({"error": True, "message": "A name is required."}), 400)

    try:
        reqBody["message"]
    except KeyError:
        return make_response(json.dumps({"error": True, "message": "A message is required."}), 400)

    # create the blab to store
    blabToAdd = {
                    "_id"      : str(uuid.uuid4()),
                    "postTime" : int(time.time()),
                    "author"   : reqBody["author"],
                    "message"  : reqBody["message"]
                }

    # add blab to mongo
    blabCollection.insert(blabToAdd)

    # really hacky workaround (need to switch _id to id before returning to user)
    blabToAdd["id"] = blabToAdd.pop("_id")

    # return our made blab
    return make_response(json.dumps(blabToAdd), 201)

# GET method to get all blabs
@flaskApp.route('/blabs', methods = ['GET'])
def getAllBlabs():
    """
    Handles GET request to get all blabs.

    :return: 200 and (json) Appropriate response as defined in Blabber specs.
    """
    # check and see if we have query argument
    if not request.query_string or request.args.get('createdSince') is None:
        createdSince = 0  # get all blabs this way
    else:
        createdSince = int(request.args.get('createdSince'))

    # workaround: use a loop to make valid JSON
    responses = "["

    for index, blab in enumerate(blabs.values()):
        # only pull relevant blabs
        if int(json.loads(blab)["postTime"]) >= createdSince:
            responses += blab
            if index != len(blabs.values()) - 1:
                responses += ", "

    responses += "]"

    return make_response(responses, 200)


# DELETE method to delete blab
@flaskApp.route('/blabs/<id>', methods = ['DELETE'])
def removeBlab(id):
    """
    Handles REMOVE request to remove specific blab at id.

    :param id: (str) UUID of blab to delete.
    :return: 200 if Blab was deleted successfully, 404 if not
    """
    # attempt to find blab
    try:
        del blabs[id]
    except KeyError:
        return make_response(json.dumps({"message": "Blab not found."}), 404)

    # otherwise, return a 200 if we didn't get an error
    return make_response(json.dumps({"message": "Blab successfully deleted."}), 200)


# if script is just run, start the app
if __name__ == "__main__":

    # if we don't find defined flask_port, use the default
    if not getenv("FLASK_PORT"):
        portEnv = 5000
    else:
        portEnv = getenv("FLASK_PORT")

    flaskApp.run(host='0.0.0.0', port=portEnv, debug=True)
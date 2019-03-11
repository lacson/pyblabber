"""
    pyblabber.py
    Jonathan Lacson
    CS 2304 Spring 2019

    Contains main entrypoint for pyblabber.
    Hosts hello world test page at /.
"""
from flask import Flask, make_response, request, render_template
from os import getenv
import json
import uuid
import time

# create Flask instance
flaskApp = Flask(__name__, template_folder="resources")

# create our empty dict of blabs
blabs = {}

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
    if not reqBody["author"]:
        return make_response(json.dumps({"error": True, "message": "An author is required."}), 400)

    if not reqBody["author"]["email"]:
        return make_response(json.dumps({"error": True, "message": "An email is required."}), 400)

    if not reqBody["author"]["name"]:
        return make_response(json.dumps({"error": True, "message": "A name is required."}), 400)

    if not reqBody["message"]:
        return make_response(json.dumps({"error": True, "message": "A message is required."}), 400)

    # otherwise, create a UUID
    # (pydoc for UUID library guarantees us uniqueness)
    uuidToAdd = str(uuid.uuid4())

    # create the blab to store
    blabToAdd = {
                    "id"       : uuidToAdd,
                    "postTime" : int(time.time()),
                    "author"   : reqBody["author"],
                    "message"  : reqBody["message"]
                }

    # turn our blab into a json object
    blabToAdd = json.dumps(blabToAdd)

    # add blab to dictionary
    blabs[uuidToAdd] = blabToAdd

    # return our made blab
    return make_response(blabToAdd, 201)

# GET method to get all blabs
@flaskApp.route('/blabs', methods = ['GET'])
def getAllBlabs():
    """
    Handles GET request to get all blabs.

    :return: 200 and (json) Appropriate response as defined in Blabber specs.
    """
    if request.args.get('createdSince'):
        # TODO: figure out this logic
        return make_response(str(list(blabs.values())), 200)

    else:
        return make_response(str(list(blabs.values())), 200)

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
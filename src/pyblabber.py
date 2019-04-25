"""
    pyblabber.py
    Jonathan Lacson
    CS 2304 Spring 2019

    Contains main entrypoint for pyblabber.
    Hosts hello world test page at /.
"""
from flask import Flask, make_response, request, render_template
import pymongo
from os import getenv
import json
import uuid
import time

def pullSecrets():
    """
    Attempts to pull username and password secrets.
    Exits script if cannot be found.

    :return: username (str) and password (str)
    """
    # try to get username
    username = extractSecret("MONGO_ROOT_USERNAME")

    # try to get password
    password = extractSecret("MONGO_ROOT_PASSWORD")

    # make sure we actually got strings
    if not username or not password:
        exit()

    else:
        return username, password


def extractSecret(file):
    """
    Attempts to pull docker secret.
    Assumes all secrets are stored in /run/secrets.

    :param file: name of file to try and read from
    :return: (str) of secret if successful, (bool False) if not
    """
    # prepend secret path to file
    file = "/run/secrets/" + file

    # make sure file exists
    if os.path.exists(file) is False:
        print("Error: could not find secret file %s, check configuration" % file)
        return False

    # if file exists, read it
    with open(file) as openedFile:
        tempStr = openedFile.read()

    # clean up string
    tempStr = tempStr.rstrip()

    # return string
    return tempStr

# create Flask instance
flaskApp = Flask(__name__, template_folder="resources")

# attempt to get our secrets
extractedUser, extractedPass = pullSecrets()

# connect to mongo server
mongo = pymongo.MongoClient('mongo', username=extractedUser,
                                     password=extractedPass,
                                     port=27017)

# make blabs callable
blabDB = mongo["blabs"]
blabCollection = blabDB["blabs"]


# perform database health check
@flaskApp.route('/status')
def healthCheck():
    """
    Simple URL to pull container health checks.

    :return: 0 if healthy, 1 if not healthy
    """
    # try to reconnect to the server (1ms timeout)
    try:
        mongo = pymongo.MongoClient('mongo', 27017, 
            serverSelectionTimeoutMS=1)
        mongo.server_info()
    except pymongo.errors.ServerSelectionTimeoutError:
        return make_response('1')
    else:
        return make_response('0')


# host our hello world html page
@flaskApp.route('/')
def home():
    """
    Responds to root on default port

    :return: served hello world web page
    """
    return render_template("hello_world.html")


# POST method to add a new blab
@flaskApp.route('/blabs', methods=['POST'])
def addBlab():
    """
    Handles POST request to add a blab.

    :return: 201 and (json) Appropriate response as defined in Blabber specs,
             400 if request schema was not valid.
    """
    # get our request data
    reqBody = request.get_json(force=True)

    # verify that we got valid inputs
    try:
        reqBody["author"]
    except KeyError:
        return make_response(json.dumps({"error": True,
                                         "message": "An author is required."}),
                                        400, {'Content-Type': 'application/json'})

    try:
        reqBody["author"]["email"]
    except KeyError:
        return make_response(json.dumps({"error": True,
                                         "message": "An email is required."}),
                                        400, {'Content-Type': 'application/json'})

    try:
        reqBody["author"]["name"]
    except KeyError:
        return make_response(json.dumps({"error": True,
                                         "message": "A name is required."}),
                                        400, {'Content-Type': 'application/json'})

    try:
        reqBody["message"]
    except KeyError:
        return make_response(json.dumps({"error": True,
                                         "message": "A message is required."}),
                                        400, {'Content-Type': 'application/json'})

    # create the blab to store
    blabToAdd = {"_id":      str(uuid.uuid4()),
                 "postTime": int(time.time()),
                 "author":   reqBody["author"],
                 "message":  reqBody["message"]}

    # add blab to mongo
    blabCollection.insert_one(blabToAdd)

    # really hacky workaround
    # (need to switch _id to id before returning to user)
    blabToAdd["id"] = blabToAdd.pop("_id")

    # return our made blab
    return make_response(json.dumps(blabToAdd), 201, {'Content-Type': 'application/json'})


# GET method to get all blabs
@flaskApp.route('/blabs', methods=['GET'])
def getAllBlabs():
    """
    Handles GET request to get all blabs.

    :return: 200 and (json) Appropriate response as defined in Blabber specs.
    """
    # check and see if we have query argument
    if not request.query_string or request.args.get('createdSince') is None:
        createdSince = 0  # get all blabs this way
    else:
        try:
            createdSince = int(request.args.get('createdSince'))
        except Exception:  # if we get garbage, don't crash
            createdSince = 0

    # get all blabs
    allBlabs = blabCollection.find({})

    # workaround: use a loop to make valid JSON
    responses = "["

    for index, blab in enumerate(allBlabs):
        # only pull relevant blabs
        if int(blab["postTime"]) >= createdSince:  # TODO: consider fixing this nonsense
            # again, correct "_id" to "id"         # PyMongo should have methods that will fix
            tempBlab = blab
            tempBlab["id"] = tempBlab.pop("_id")

            # add blab to our string
            responses += json.dumps(tempBlab)

            # only add comma if it's not the last blab
            if index != allBlabs.count() - 1:
                responses += ", "

    responses += "]"

    return make_response(responses, 200, {'Content-Type': 'application/json'})


# DELETE method to delete blab
@flaskApp.route('/blabs/<id>', methods=['DELETE'])
def removeBlab(id):
    """
    Handles REMOVE request to remove specific blab at id.

    :param id: (str) UUID of blab to delete.
    :return: 200 if Blab was deleted successfully, 404 if not
    """
    # attempt to delete said blab if we find a matching ID
    if blabCollection.find_one_and_delete(({'_id': id})) is None:
        return make_response(json.dumps({"message": "Blab not found."}),
                                        404, {'Content-Type': 'application/json'})

    # otherwise, return a 200 if we didn't get an error
    return make_response(json.dumps({"message": "Blab successfully deleted."}),
                                    200, {'Content-Type': 'application/json'})


# if script is just run, start the app
if __name__ == "__main__":

    # if we don't find defined flask_port, use the default
    if not getenv("FLASK_PORT"):
        portEnv = 5000
    else:
        portEnv = getenv("FLASK_PORT")

    flaskApp.run(host='0.0.0.0', port=portEnv, debug=True)

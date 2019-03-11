"""
    pyblabber.py
    Jonathan Lacson
    CS 2304 Spring 2019

    Contains main entrypoint for pyblabber.
    Hosts hello world test page at /.
"""
from flask import Flask, render_template
from os import getenv
import json

# create Flask instance
flaskApp = Flask(__name__, template_folder="resources")

# host our hello world html page
@flaskApp.route('/')
def home():
    """
    Responds to port 5000 (Flask default)

    :return: served hello world web page
    """
    return render_template("hello_world.html")

# POST method to add a new blab
@flaskApp.route('/blabs', methods = ['POST'])
def addBlab():
    """
    Handles POST request to add a blab.

    :return: 201 and (json) Appropriate response as defined in Blabber specs.
    """
    pass # TODO: writeme

# GET method to get all blabs
@flaskApp.route('/blabs', methods = ['GET'])
def getAllBlabs():
    """
    Handles GET request to get all blabs.

    :return: 200 and (json) Appropriate response as defined in Blabber specs.
    """
    pass # TODO: writeme

# DELETE method to delete blab
@flaskApp.route('/blabs/<id>', methods = ['REMOVE'])
def removeBlab(id):
    """
    Handles REMOVE request to remove specific blab at id.

    :param id: ID of blab to delete.
    :return: 200 if Blab was deleted successfully, 404 if not
    """
    pass # TODO: writeme


# if script is just run, start the app
if __name__ == "__main__":

    # if we don't find defined flask_port, use the default
    if not getenv("FLASK_PORT"):
        portEnv = 5000
    else:
        portEnv = getenv("FLASK_PORT")

    flaskApp.run(host='0.0.0.0', port=portEnv, debug=True)
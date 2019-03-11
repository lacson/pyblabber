"""
    pyblabber.py
    Jonathan Lacson
    CS 2304 Spring 2019

    Will contain main entrypoint for pyblabber.
    Currently hosts hello world test.
"""
from flask import Flask, render_template
from os import getenv

# create Flask instance
flaskApp = Flask(__name__, template_folder="resources")

# host our hello world html page
@flaskApp.route('/')
def home():
    """
    Responds to port 5000 (Flask default)

    :return: served webpage
    """
    return render_template("hello_world.html")


# if script is just run, start the app
if __name__ == "__main__":

    # patchy workaround to set port
    if not getenv("FLASK_PORT"):
        portEnv = 5000
    else:
        portEnv = getenv("FLASK_PORT")

    flaskApp.run(host='0.0.0.0', port=portEnv, debug=True)
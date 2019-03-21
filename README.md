# pyblabber
Implementation of Blabber API in Python  
(Semester Project for CS 2304 Spring 2019, Virginia Tech)

## API Support

Pyblabber is designed to support the Blabber API. 

A more in-depth list of the methods can be found 
[here](https://cs2304.mikesir87.io/spec/).

## Setup

It is possible to run `pyblabber` natively or containerized in Docker.

### System Requirements and Defaults

* Python 3  
* Flask Library

By default, `pyblabber` runs on port `5000` (due to it being the default
of Flask) but it is perfectly adjustable.

### Native Setup

(NOTE: This is perfectly possible and theoretically should work just fine, but
you will have no ability to change the port used without editing the code 
directly. I make no guarantees of functionality since the preferred method of
running pyblabber is through Docker.)

A `requirements.txt` file required by `pip` is included in the `src/` folder.
Once the required libraries are installed, just execute `python3 src/pyblabber.py`.

### Docker Setup

For convenience, the port used is a variable and can be changed 
in the Dockerfile. It is copied into the created image as an environment
variable.

A Docker image can be created and run using the included Dockerfile.
Commands for reference:

    $ docker build -t pyblabber:latest .
    $ docker container run -p <port>:<port> -it pyblabber

## Roadmap

Just a short list of things to do:

* [x] Handle custom time specification in `GET` method
* [ ] Abstract `GET` method logic away
* [ ] Write integration test script (and maybe containerize it)
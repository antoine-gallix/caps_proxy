# Caps Proxy

## What is it?

Caps Proxy is an application that serves as a proxy to the shoutcloud service. You send it text, it let shoutcloud uppercase it and sends you the result back.

    json query:
        {'input':'please caps me!'}
    json response:
        {'input':'please caps me!',
        'output':'PLEASE CAPS ME!'}

It's a JSON only service. Even error messages should be json only.

## Design notes

While it certainly is possible to write everything more simply, I just started from a flask rest api template I developed some time ago while learning the framework, and pruned it to keep only needed features. Hence some fancy stuff like json errors I wouldn't normally have bothered to write for a single-endpoint caps service. But as I had the snippets ready and tested, I just used them.

It makes use of the application factory pattern in `app.py`. The caps service code is in a separate file `caps.py` and make use of flask blueprint. Application administration uses [`invoke`](http://docs.pyinvoke.org/en/latest/index.html#) package and commands are defined in the `tasks.py` file. Commands are run as follow: `invoke run dev` or `invoke build-image`.

## Setup

Start a new virtualenv with python 3 and install requirements:

    pip install -r requirements

## Run Tests

    invoke tests

## Run Server Manually

    invoke run dev

Then attack the server on localhost:5000 with json inputs like `{'input':'please caps me'}`. Application logs are displayed on terminal and also recorded to `debug.log` at application root level.

Example with httpie:

    ~/projects/infarm > http post localhost:5000/to_caps input=plic
    HTTP/1.0 200 OK
    Content-Length: 43
    Content-Type: application/json
    Date: Sun, 25 Mar 2018 23:50:52 GMT
    Server: Werkzeug/0.14.1 Python/3.5.2

    {
        "input": "plic",
        "output": "PLIC"
    }


## Run Server In A Container

With docker installed:

    invoke build-image
    invoke run-image

Then test the same way as for the local server.

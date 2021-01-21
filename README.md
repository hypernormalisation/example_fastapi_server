# example_fastapi_server
An example server application and environment file using the ASGI
FastAPI framework, running on Uvicorn.

## WSGI and ASGI

First, let's understand the python web ecosystem a little more. This is
a *very non-exhaustive summary!*

### WSGI

Web Server Gateway Interface (WSGI) is a "simple convention for web
servers to forward requests to web applications or frameworks written in
Python".

From wiki:
> In 2003, Python web frameworks were typically written against only
> CGI, FastCGI, mod_python, or some other custom API of a specific web
> server

Quoting PEP 333:
> By contrast, although Java has just as many web application frameworks
> available, Java's "servlet" API makes it possible for applications
> written with any Java web application framework to run in any web
> server that supports the servlet API.
>

Wiki again:
> WSGI was thus created as an implementation-agnostic interface between
> web servers and web applications or frameworks to promote common
> ground for portable web application development.



Commonly, a server application is comprised of some kind of framework
and a particular server. Some you may have heard of:

- Flask is a web microframework, commonly run on a WSGI server like
  Gunicorn.
- Django is an extensive web framework, which can run on WSGI servers
  (but also ASGI servers).
- Tornado is both a non-blocking WSGI server and web application
  framework. You may have seen it used in Jupyter, where it is the
  server of choice for HTTP requests.

### ASGI

WSGI was developed in the days before async-capability came to Python.

The *Asynchronous Server Gateway Interface* ASGI was created as a
spiritual successor to WSGI for asynchronous python applications.

Some you may have heard of:
- Daphne is the current ASGI reference server, written in Twisted and
  maintained as part of the Django Channels project.
- Uvicorn is an ASGI server that scores very high on performance.
- as we mentioned above, Django can run on WSGI servers.
- Sanic is a combined async web framework and server.
- FastAPI is a high-performance async web framework, typically run on
  Uvicorn.

Now you know some of the history, let me sell you on FastAPI.

## Why FastAPI?

FastAPI is a modern, fast, robust, and very flexible framework for
building APIs that document themselves.

If you've used Flask and Gunicorn, you should feel very at home.

FastAPI is built on the OenAPI standard for documentation, and uses
Python 3.8+'s own built-in type checking to validate data and populate
documentation on your APIs.

## Example Server

We include an example server, in `web_app/main.py`, and a conda env file
`conda_env.yml`.

There are two endpoints:

- GET /public/test: a simple test to return a message
- POST /merge: an endpoint to simulate the manipulation of some shared
  resource

If you POST to merge with the expected format (for that see Read the
Docs!) then we simulate a shared resource being used for 10 seconds.

If the shared resource is free, we return a simple message confirming
the merge is in process.

If the shared resource is not free, we return a 401 code with the detail
that the shared resource is in use.

### Environment

With conda installed, a simple

`conda env create -f conda_env.yml`

will create an env called "example_fastapi_server":

`conda activate example_fastapi_server`.

If you would prefer not to use conda, create a virtualenv and run:

```bash
pip install fastapi[all] 
```

### Run

To run the server:

```bash
uvicorn web_app.main:app
```

### Read the docs

To read your self-generating documentation, go to `127.0.0.0:8000/docs`
in your web browser of choice.

To download the OpenAPI json specification for your API, to
automatically interface client applications or the like, just request
from `http://127.0.0.1:8000/openapi.json`


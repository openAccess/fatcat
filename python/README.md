
## Fatcat Python Code

This directory contains python code for the fatcat project: a web interface
(`fatcat_web`) and a series of utilities and worker processes (`fatcat_tools`).
These depend on the API client library (`fatcat_client`, see below).

Most of this code is an "application" which is tightly interwoven and intended
to be run from this directory, but the client library is distributed on
pypi.org.

## API Client Library

The auto-generated python client library for the fatcat API lives under
`../fatcat_client`. It includes entity model objects and functions to call all
API endpoints; see the `README.md` for details.

To re-generate swagger-codegen python client library (requires docker installed
locally):

    ./codegen_python_client.sh

## Web Interface

This project uses `pipenv` to manage dependencies, and assumes Python 3.5
(which pipenv may install if you are running a different local version; see
notes in Pipfile). You can can install `pipenv` with `pip`. You may want to set
the `PIPENV_VENV_IN_PROJECT` environment variable on your development machine
(see pipenv docs for details).

To just run the web interface (which will try to connect to a back-end API
server on the same machine by default), use:

    # will listen on http://localhost:9810 by default
    pipenv run fatcat_webface.py

Almost all configuration is done via environment variables; see `example.env`
for a list of settings. If you copy this file to `.env` it will be sourced by
`pipenv` automatically; you can also load it in your shell like `source .env`.

## Running Tests

Many (though not all) python tests depend on access to a local running API
server (the `fatcatd` rust daemon, code in `../rust/`), which itself depends on
a local PostgreSQL database server. Tests will fail if this endpoint isn't
found. See the README there to get that set up first. The CI integration tests
build and start this daemon automatically.

To run the python tests (with `fatcatd` running locally on port 9411):

    pipenv install --dev
    pipenv run pytest

To calculate code coverage (of python code):

    pipenv run pytest --cov --cov-report html

To run 'lint' on the code base (note that this is pretty noisy and isn't
enforced by CI yet):

    pipenv run pylint fatcat*.py fatcat_tools fatcat_web

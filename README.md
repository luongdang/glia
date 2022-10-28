# ldang-glia

This repo contains my Skill Assessment test for the Infrastructure Engineer position at Glia. As per requirements, this repo contains 3 parts:

1. An API server, written in Python and FastAPI
2. A docker container
3. A Helm chart for deployment

## Running the API server locally

Prerequisites:
* This server requires Python 3.9
* [`pyenv`](https://github.com/pyenv/pyenv) (or its Windows equivalent [`pyenv-win`](https://github.com/pyenv-win/pyenv-win)) are highly recommended to manage multiple Python versions.
* The repo uses `poetry` to manage its dependencies. Follow the [installation instructions](https://python-poetry.org/docs/#installation) to install it on your system.

To initialize the project, `cd` to where you cloned this repo and activate the virtual environment:

```bash
cd path/to/ldang-glia
poetry install
```

*(All subsequent commands assume that you are in `ldang-glia` as your working folder and have activated the virtual environment)*

You can then start the API server locally:

```bash
# Activate the Poetry environment
poetry shell

# Start the server, running on port 8000 by default
uvicorn app:app
```

Visit the app by navigating to [http://localhost:8000](http://localhost:8000) in your browser. You can try a few operations:

```txt
http://localhost:8000/jumble/{word}
    randomly rearrange the characters in 'word'

http://localhost:8000/audit?n={n}
    return the last n requests made to the server
    If n is not specified, default to 10.

http://localhost:8000/docs
    OpenAPI specs / Swagger documentation for the API
```

### Developing and updating the API

Development settings for VS Code are included in the repo. If you use VS Code, just open the repo and press `F5` to start the API server in debug mode. 

If you use other IDEs, make sure to point it to the appropriate virtual environment.

For testing, VS Code provides integrated testing functionalities. Simply switch to the Testing tab to discover and run tests. You can also run test manually from the command line:

```bash
# Activate the virtual environment
poetry shell

# Run tests
pytest tests/
```

## Dockerize the application

```bash
# Build the image
docker image build -t ldang/glia:latest .

# Start a new container
# This command will print the Container ID to stdout
docker run -dp 8000:8000 --rm --name glia luongdang/glia

# Now you can open the app at http://localhost:8000
# When you are done experimenting with the app, stop
# the container
docker stop <container_id>
```

## Deploy to Kubernetes

TBA

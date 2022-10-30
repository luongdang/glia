# ldang-glia

> **Note to Glia reviewer:** if you check the commit history, you can find that I spent more than 2 hours completing this assessment. As I noted in my original submission, Helm chart wasn't my forte. However, I'm committed to give this assessment my best effort. It may be late, but it wil be complete. It may be shaky but it will be a learning experience. Only by stepping out of comfort zone will I learn and grow.
<br><br>
All 3 requirements are now complete and ready for your review.

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

Download & install Docker Desktop. Launch Docker and use the following commands to test a Dockerized version of the app:

```bash
# Build the image
docker image build -t luongdang/glia:latest .

# Start a new container
# This command will print the Container ID to stdout.
docker run -dp 8000:8000 --rm --name glia luongdang/glia

# Now you can open the app at http://localhost:8000
# When you are done experimenting with the app, stop
# the container.
docker stop <container_id>
```

Now you can push the image to Docker hub:

```bash
docker image push luongdang/glia:latest
```

## Deploy to Kubernete

**Prerequisite**: install `minikube` and `kubectl`.

```bash
# Start minikube with 2 nodes: 1 master and 1 worker.
minikube start --nodes 2

# Check that the nodes are running
minikube status
# If you get something like below, the nodes are good:
# minikube
# type: Control Plane
# host: Running
# kubelet: Running
# apiserver: Running
# kubeconfig: Configured
#
# minikube-m02
# type: Worker
# host: Running
# kubelet: Running

# Install the Helm chart
helm install luongdang-glia helm-chart

# Check the pods and wait until it's ready
kubectl get pods

# Setup the port forward from the local computer to the pod
POD_NAME=$(
kubectl get pods \
    -l "app.kubernetes.io/name=luongdang-glia" \
    -o jsonpath="{.items[0].metadata.name}"
)
# Forward port 8000 on the local PC to port 8000 in the pod
kubectl port-forward $POD_NAME 8000:8000
```

Now you can visit the application in the browser at `http://localhost:8000`.
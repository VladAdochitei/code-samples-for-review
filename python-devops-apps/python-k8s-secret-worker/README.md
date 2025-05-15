# sw-python-k8s-secret-worker
> SW 2024 January 11 (Finished) - Preliminary version


## Description
Kubernetes Job written in Python and containerized with docker, its purpose is toread secrets from the cluster and later export them in the desired form (ConfigMap, etc..).


## Configure minikube 
First you'll have to start the minikube cluster in order to be able to use the solution: https://minikube.sigs.k8s.io/docs/start/

## Pushing the docker container image
then you'll need to build and push the docker container image to a remote repository (best practice)

### Build the docker image
```sh
docker build -t python-k8s-secret-worker:0.0.1
```

### Run the docker container locally

```sh
docker run \
  -e SECRET_NAME=my-secret \
  -e SECRET_NAMESPACE=default \
  python-k8s-secret-worker:0.0.1

```

---------------------------------------
Here we'll have to review the format of the docker image registry

### Login into the image registry
```sh
docker login dockerhub -u "<username>" -p "<password>"
```

### Tag the local image
```sh
docker tag python-k8s-secret-worker:0.0.1 dockerhub/VladAdochitei/python-k8s-secret-worker:0.0.1
```

### Push the image
```sh
docker push dockerhub/VladAdochitei/python-k8s-secret-worker:0.0.1
```
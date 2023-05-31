# Dev

## Minikube

### Create a Cluster

1. Start the Minikube Cluster

   ```shell
   minikube start --cpus 8 --memory 16000
   ```

2. Enable ingress addon

   ```shell
   minikube addons enable ingress
   ```

### Delete a Cluster

It may be necessary to start with a fresh cluster. Delete your cluster with:
```shell
minikube delete
```

This may take some time.


3. Start tilt

   ```shell 
   tilt up
   ```

## Update images

This repo includes and auto image updater that will fetch the latest version of every virtool image and update their respective YAML files.

### Requirements

  - Have poetry installed on your local machine
  - Python +3.10

### Usage

1. Install dependencies
   ```shell
   poetry install
   ```
2. Run the updater

   ```shell 
   poetry run python ./update/run.py
   ```



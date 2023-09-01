# Dev



## Cluster setup

### Dependencies

- Docker engine
- Minikube
- Tilt
- Kubectl
- Helm
- nfs-kernel-server
- `git`

### Initial Setup

1. Clone the repository to your local machine
   ```
   git clone https://github.com/virtool/dev.git
   ```
   
2. Add the following line to your `/etc/hosts` file to enable access to 
   the cluster from your local machine
   ```
   192.168.49.2 virtool.local
   ```

### Create a Cluster

1. Start the Minikube Cluster

   ```shell
   minikube start --cpus 8 --memory 16000
   ```

2. Enable ingress addon

   ```shell
   minikube addons enable ingress
   ```
   
3. Navigate into your `dev` directory and start tilt with the following command

   ```shell 
   tilt up 
   ```
   
In a few minutes you cluster should be reachable at: [http://virtool.local](http://virtool.local)


### Delete a Cluster

It may be necessary to start with a fresh cluster. Delete your cluster with:
```shell
minikube delete
```

This may take some time. Once it is complete, you can start a new cluster following the
instructions for creating a cluster.



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



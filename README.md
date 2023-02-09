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

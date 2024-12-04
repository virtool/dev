#!/bin/bash

echo "Deleting any existing Minikube cluster..."
minikube delete --purge=true

echo "Starting Minikube for first time..."
minikube start --cpus 8 --memory 16000

echo "Enabling Minikube addons..."
minikube addons enable ingress
minikube addons enable metrics-server

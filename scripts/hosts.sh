# Get the IP address of the minikube cluster.
MINIKUBE_IP=$(minikube ip)

# Delete the existing line for virtool.local in the hosts file.
sudo sed -i '/virtool.local/d' /etc/hosts

# Add the minikube IP to the hosts file.
sudo sed -i "/^127\.0\.1\.1/a $MINIKUBE_IP\tvirtool.local" /etc/hosts

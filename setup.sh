#!/bin/bash
set -e
CLUSTER_NAME="training-cluster"
cat <<EOC > kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30080
    hostPort: 30080
    protocol: TCP
EOC
if kind get clusters | grep -q "^\$CLUSTER_NAME\$"; then
  echo "Le cluster \$CLUSTER_NAME existe déjà."
else
  kind create cluster --name "\$CLUSTER_NAME" --config kind-config.yaml
fi
kubectl cluster-info
helm upgrade --install mon-application ./mon-application --namespace mon-application --create-namespace
kubectl wait --for=condition=Ready pod -l app=nginx -n mon-application --timeout=120s

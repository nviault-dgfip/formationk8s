#!/bin/bash
set -e

CLUSTER_NAME="training-cluster"

echo "--- 1. Création de la configuration KIND pour automatisation ---"
cat <<EOF > kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30080
    hostPort: 30080
    protocol: TCP
EOF

echo "--- 2. Création du cluster KIND '$CLUSTER_NAME' ---"
if kind get clusters | grep -q "^$CLUSTER_NAME$"; then
  echo "Le cluster $CLUSTER_NAME existe déjà."
else
  kind create cluster --name "$CLUSTER_NAME" --config kind-config.yaml
fi

echo "--- 3. Vérification de l'accès ---"
kubectl cluster-info

echo "--- 4. Installation du chart Helm ---"
helm upgrade --install mon-application ./mon-application \
  --namespace mon-application \
  --create-namespace

echo "--- 5. Attente des pods ---"
kubectl wait --for=condition=Ready pod -l app=nginx -n mon-application --timeout=120s

echo ""
echo "===================================================="
echo "Déploiement terminé !"
echo "Accédez à l'application sur : http://localhost:30080"
echo "N'oubliez pas de configurer l'IP du formateur dans mon-application/values.yaml si nécessaire."
echo "===================================================="

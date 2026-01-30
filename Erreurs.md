# Guide de Débogage - Laboratoire Kubernetes

Ce document récapitule les erreurs volontairement introduites dans le projet pour l'exercice de débogage.

---

## 1. Erreur d'Image (ImagePullBackOff)

- **Fichier** : `values.yaml`
- **Erreur** : `tag: "1.26-2"` (au lieu de `1.26.2`).
- **Notion testée** : Cycle de vie des Pods et récupération d'images.
- **Symptôme** : Les pods restent en état `ImagePullBackOff` ou `ErrImagePull`.
- **Commandes de débogage** :
  - `kubectl get pods -n mon-application`
  - `kubectl describe pod <nom-du-pod> -n mon-application` (regarder la section Events)
- **Correction** : Remplacer `1.26-2` par `1.26.2` dans `values.yaml`.

---

## 2. Incohérence de Sélecteur Service

- **Fichier** : `templates/service.yaml`
- **Erreur** : `selector: app: nginx-web` (au lieu de `nginx`).
- **Notion testée** : Mise en relation (Label Selector) entre Services et Pods.
- **Symptôme** : Le service existe mais ne redirige vers rien. L'accès à `localhost:30080` ne fonctionne pas (timeout ou connexion refusée).
- **Commandes de débogage** :
  - `kubectl get endpoints -n mon-application` (affichera `<none>`)
  - `kubectl describe svc nginx-svc -n mon-application`
- **Correction** : Changer le sélecteur pour `app: nginx` dans `templates/service.yaml`.

---

## 3. Erreur de Namespace

- **Fichier** : `templates/deployment.yaml`
- **Erreur** : `namespace: mon-app` (hardcodé) au lieu d'utiliser le namespace cible `mon-application`.
- **Notion testée** : Isolation des ressources par Namespace.
- **Symptôme** : L'installation Helm échoue avec un message indiquant que le namespace `mon-app` n'existe pas, ou le déploiement ne se retrouve pas dans le même namespace que le reste.
- **Commandes de débogage** :
  - `kubectl get all -A` (pour chercher où sont passées les ressources)
  - `helm install ...` (lire attentivement le message d'erreur)
- **Correction** : Supprimer la ligne `namespace: mon-app` ou la remplacer par `namespace: mon-application` (ou mieux, laisser Helm gérer via le template).

---

## 4. Mauvais Port Cible (TargetPort)

- **Fichier** : `templates/service.yaml`
- **Erreur** : `targetPort: 8080` (au lieu de `80`).
- **Notion testée** : Configuration réseau des Services (Port vs TargetPort).
- **Symptôme** : Le service a des endpoints valides, mais la connexion échoue car NGINX écoute sur le port 80, pas 8080.
- **Commandes de débogage** :
  - `kubectl describe pod <nom-du-pod> -n mon-application` (vérifier le port du conteneur)
  - `kubectl logs <nom-du-pod> -n mon-application`
- **Correction** : Remettre `targetPort: 80` dans `templates/service.yaml`.

---

## 5. Erreur de Montage ConfigMap (subPath)

- **Fichier** : `templates/deployment.yaml`
- **Erreur** : `subPath: welcome.html` (au lieu de `index.html`).
- **Notion testée** : Volumes et ConfigMaps.
- **Symptôme** : Les pods sont en état `CreateContainerConfigError`.
- **Commandes de débogage** :
  - `kubectl describe pod <nom-du-pod> -n mon-application` (message indiquant que la clé n'existe pas dans la ConfigMap)
  - `kubectl get configmap mon-application-config -n mon-application -o yaml`
- **Correction** : Remettre `subPath: index.html` dans `templates/deployment.yaml`.

# Pipeline CI/CD Python

Ce projet utilise GitHub Actions pour automatiser le build, les tests et le push d'une image Docker d'une application Python.

## Fonctionnalités

- Construction d'une image Docker
- Exécution des tests dans un conteneur
- Push de l'image sur Docker Hub

## Configuration

Avant d'exécuter le pipeline, assurez-vous d'avoir configuré :

1. **Variables GitHub** :

   - `DOCKERHUB_USERNAME` : Nom d'utilisateur Docker Hub

2. **Secrets GitHub** :
   - `DOCKERHUB_TOKEN` : Token d'accès Docker Hub

## Workflow GitHub Actions

Le workflow est défini dans `.github/workflows/pipeline.yml` et s'exécute sur chaque push vers `master`.

### Étapes du Workflow

1. **Checkout** du code source
2. Connexion à Docker Hub
3. Build de l'image Docker (`server-python-app`)
4. Exécution des tests dans un conteneur
5. Tag de l'image Docker
6. Push de l'image vers Docker Hub

## Commandes Manuelles

Si besoin, vous pouvez exécuter les commandes suivantes localement :

```sh
# Build de l'image
docker build -t server-python-app .

# Exécution des tests
docker run --rm server-python-app pytest tests/

# Tag de l'image
docker tag server-python-app DOCKERHUB_USERNAME/server-python-app:latest

# Push vers Docker Hub
docker push DOCKERHUB_USERNAME/server-python-app:latest
```

Remplacez `DOCKERHUB_USERNAME` par votre identifiant Docker Hub.

## Licence

Ce projet est sous licence MIT.

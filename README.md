# MLflow Experiment Tracking & Model Deployment

## 📌 Objectif
Mettre en place **MLflow** pour :
1. **Suivre les expériences de machine learning** : enregistrement des hyperparamètres, métriques et modèles.
2. **Gérer un registre de modèles** pour identifier et valider les meilleurs modèles.
3. **Déployer le modèle dans un conteneur Docker** pour une utilisation en production.

---

## 🛠️ Installation

Avant de commencer, installez **MLflow** et ses dépendances :

```bash
pip install mlflow
```

Pour utiliser MLflow avec **Scikit-learn**, installez également :

```bash
pip install scikit-learn
```

---

## 🔹 Étape 1 : Suivi des Expériences avec MLflow

### Démarrer l'interface utilisateur MLflow

```bash
mlflow ui
```

Cela ouvre une interface sur `http://127.0.0.1:5000/`, où vous pouvez visualiser les expériences.

### Ajouter le suivi MLflow dans le code

Dans votre script d'entraînement du modèle (`train.py` par exemple) :

```python
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd

# Charger les données
df = pd.read_csv("housing_data.csv")
X = df.drop(columns=["median_house_value"])
y = df["median_house_value"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Activer MLflow
tracking_uri = "http://127.0.0.1:5000"
mlflow.set_tracking_uri(tracking_uri)
mlflow.set_experiment("housing-price-prediction")

with mlflow.start_run():
    # Définir et entraîner le modèle
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Prédire et évaluer
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    
    # Logger les paramètres et métriques
    mlflow.log_param("model", "LinearRegression")
    mlflow.log_metric("mse", mse)
    
    # Enregistrer le modèle dans MLflow
    mlflow.sklearn.log_model(model, "housing_model")
```

---

## 🔹 Étape 2 : Enregistrement du Modèle dans le Model Registry

Un modèle bien performant peut être **ajouté au registre** via l'interface MLflow ou en utilisant le code suivant :

```bash
mlflow models register -m runs:/<run_id>/housing_model -n housing_model_registry
```

Remplacez `<run_id>` par l’ID du run MLflow contenant le modèle à enregistrer.


---

## 🔹 Étape 3 : Construire et Dockeriser le Modèle

MLflow facilite le déploiement avec Docker :

```bash
mlflow models build-docker -m "models:/housing_model_registry/Production" -n housing-model
```

Cela crée une image Docker `housing-model` prête à être déployée.

---

## 🔹 Étape 4 : Déployer le Modèle avec Docker Compose

Créez un fichier `docker-compose.yaml` :

```yaml
version: '3'
services:
  housing-model:
    image: housing-model
    ports:
      - "5001:8080"
    environment:
      - MLFLOW_TRACKING_URI=http://127.0.0.1:5000
```

Lancez le service :

```bash
docker-compose up -d
```

Le modèle est maintenant disponible sur `http://127.0.0.1:5001/predict`.



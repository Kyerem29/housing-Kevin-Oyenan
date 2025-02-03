import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.datasets import load_diabetes
import pandas as pd

# Charger un dataset (Diabetes dataset de Scikit-learn)
data = load_diabetes()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

# Séparation des données en train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Début de l'expérience MLflow
with mlflow.start_run():
    # Définition du modèle
    model = LinearRegression()

    # Enregistrement des hyperparamètres
    mlflow.log_param("fit_intercept", model.fit_intercept)
    
    # Entraînement du modèle
    model.fit(X_train, y_train)

    # Prédictions sur le test set
    y_pred = model.predict(X_test)

    # Calcul des métriques
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Enregistrement des métriques
    mlflow.log_metric("MSE", mse)
    mlflow.log_metric("R2 Score", r2)

    # Enregistrement du modèle
    mlflow.sklearn.log_model(model, "linear_regression_model")

    print(f"Modèle enregistré avec MSE={mse:.4f} et R2={r2:.4f}")

print("Fin de l'expérience. Vérifiez MLflow UI pour voir les logs.")

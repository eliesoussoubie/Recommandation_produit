from flask import Flask, request, jsonify
import joblib
import numpy as np


# Charger le modèle KNN et le scaler
knn_model = joblib.load('knn_model_compressed.pkl')
scaler = joblib.load('scaler.pkl')

app = Flask(__name__)


# Route d'accueil
@app.route('/')
def home():
    return "Bienvenue sur l'API de recommandation de produits!"


# Route pour le favicon.ico
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')  # Servir l'icône depuis le dossier 'static'


# Route pour prédiction
@app.route('/predict', methods=['POST'])
def predict():
    # Récupérer les données envoyées par l'utilisateur
    data = request.get_json()  # Le client doit envoyer les données sous forme de JSON
    features = np.array(data['features']).reshape(1, -1)  # Les données envoyées doivent être un tableau

    # Appliquer le scaling
    features_scaled = scaler.transform(features)

    # Prédiction avec le modèle KNN
    prediction = knn_model.predict(features_scaled)

    # Retourner la prédiction sous forme JSON
    return jsonify({'prediction': prediction.tolist()})


if __name__ == '__main__':
    app.run(debug=True)

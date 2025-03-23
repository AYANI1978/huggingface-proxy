
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/ai", methods=["POST"])
def ai_proxy():
    data = request.get_json()
    texte = data.get("texte", "").strip()

    if not texte:
        return jsonify({"error": "Texte manquant"}), 400

    prompt = f"""Tu es un assistant RH. Reformule et structure cette offre d’emploi brute dans ce format :
- Intitulé du poste
- Missions
- Compétences requises
- Durée
- Lieu
- Conditions
- Profil recherché

Offre :
"""{texte}""""""

    try:
        response = requests.post(
            "https://hf.space/embed/HuggingFaceH4/zephyr-7b-alpha/api/predict/",
            json={"data": [prompt]},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        hf_result = response.json()
        return jsonify({"texte": hf_result.get("data", [""])[0]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

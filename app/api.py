import logging
import requests
from flask import Blueprint, request, jsonify
from app.config import Config

api = Blueprint('api', __name__, url_prefix='/api')

@api.route("/search_cigar")
def search_cigar():
    name = request.args.get("name", "").strip()
    if not name:
        return jsonify([])

    url = "https://cigars.p.rapidapi.com/cigars"
    headers = {
        "x-rapidapi-key": Config.RAPIDAPI_KEY,
        "x-rapidapi-host": Config.RAPIDAPI_HOST
    }
    params = {"page": "1", "name": name}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return jsonify(response.json().get("cigars", []))
    except requests.RequestException as e:
        logging.error("API FOUT: %s", str(e))
        return jsonify({"error": str(e)}), 500

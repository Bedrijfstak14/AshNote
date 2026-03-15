import logging
import requests
from flask import Blueprint, request, jsonify
from app.config import Config

logger = logging.getLogger(__name__)

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/search_cigar")
def search_cigar():
    name = request.args.get("name", "").strip()
    if not name:
        return jsonify([])

    if not Config.RAPIDAPI_KEY:
        logger.warning("RAPIDAPI_KEY is niet ingesteld — externe zoekfunctie niet beschikbaar.")
        return jsonify([])

    url = "https://cigars.p.rapidapi.com/cigars"
    headers = {
        "x-rapidapi-key": Config.RAPIDAPI_KEY,
        "x-rapidapi-host": Config.RAPIDAPI_HOST,
    }
    params = {"page": "1", "name": name}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        return jsonify(response.json().get("cigars", []))
    except requests.RequestException:
        logger.exception("Fout bij ophalen cigardata voor naam='%s'.", name)
        return jsonify({"error": "Externe zoekfunctie is momenteel niet beschikbaar."}), 503

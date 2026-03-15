import os
import secrets
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class Config:
    _secret_key = os.getenv("SECRET_KEY")
    if not _secret_key:
        _secret_key = secrets.token_hex(32)
        logger.warning(
            "SECRET_KEY niet ingesteld in .env — tijdelijke sleutel wordt gebruikt. "
            "Stel SECRET_KEY in voor stabiele sessies."
        )
    SECRET_KEY = _secret_key

    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:////app/data/cigars.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "data", "uploads")

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max upload
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
    RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "cigars.p.rapidapi.com")

    WTF_CSRF_ENABLED = True

    @staticmethod
    def init_app(app):
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        app.config["UPLOAD_FOLDER"] = Config.UPLOAD_FOLDER

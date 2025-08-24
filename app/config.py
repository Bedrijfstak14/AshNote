import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "geheim")
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    SQLALCHEMY_DATABASE_URI = "sqlite:////app/data/cigars.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Get the project root directory (parent of app directory)
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "data", "uploads")
    
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
    RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "cigars.p.rapidapi.com")
    
    @staticmethod
    def init_app(app):
        # Ensure upload folder exists
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        app.config["UPLOAD_FOLDER"] = Config.UPLOAD_FOLDER

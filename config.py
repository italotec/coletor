import os

# BASE_DIR = ...\system-flask
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# PARENT_DIR = ...\Desktop
PARENT_DIR = os.path.dirname(BASE_DIR)

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-now")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "app.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # externo/auth/usernames.dat is sibling of system-flask
    USERNAMES_DAT = os.environ.get(
        "USERNAMES_DAT",
        os.path.join(PARENT_DIR, "zphisher", "auth", "usernames.dat")
    )

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate   # ✅ ADD THIS

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get(
    "SECRET_KEY", "dev-secret"
)

# ---------------- PostgreSQL Setup ----------------
DATABASE_URL = os.getenv("DATABASE_URL")  # Render provides this

if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://", "postgresql://", 1
        )
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
    # Local PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        "postgresql://postgres:2003@localhost:5433/flaskdb"
    )

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ---------------- Extensions ----------------
db = SQLAlchemy(app)
migrate = Migrate(app, db)   # ✅ VERY IMPORTANT
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# ---------------- Mail Setup ----------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_USER')
mail = Mail(app)

# ---------------- Routes ----------------
from flaskblog import routes

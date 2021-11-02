from flask import Flask
from config import Config

app = Flask(__name__)       # constructor
app.config.from_object(Config)

from app import routes
from flask import Flask

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = r"C:\Users\ti02\Desktop\teste"
from .Routes import Routes
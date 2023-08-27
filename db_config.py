
from flask import Flask


app = Flask(__name__)

app.config['SECRET_KEY'] = 'dronerecog'
app.config['UPLOAD_FOLDER'] = 'static/files'


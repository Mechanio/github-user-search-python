from flask import Flask
from secrets import secret_key
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key  # secret key in private file

from routes import main

app.register_blueprint(main)

if __name__ == '__main__':
    app.run()

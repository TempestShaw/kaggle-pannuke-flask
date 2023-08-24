from flask import Flask, redirect, url_for, render_template, request, session
import os
from function import *
from api import api_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # set key for session
app.register_blueprint(api_blueprint)


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

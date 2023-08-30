from flask import Flask, redirect, url_for, render_template, request, session
from flask_caching import Cache
from function import *
from api import api_blueprint
import os
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.config['SECRET_KEY'] = os.urandom(24)  # set key for session
app.register_blueprint(api_blueprint)
df_ttype = DataInit()


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':

    app.run()

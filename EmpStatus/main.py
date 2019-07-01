import os
from flask import Flask, redirect, url_for
import db, auth

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)
# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db.init_app(app)
app.register_blueprint(auth.bp)

@app.route("/")
def home():
    return redirect(url_for("auth.register"))

if __name__ == "__main__":
    app.run(debug = True)

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/linstead/Dropbox/apps/pandachrome/sqlite.db'

from pandachrome import views
#from pandachrome.views import api
#app.register_blueprint(api)

db = SQLAlchemy(app)
#app.run(debug=app.config["DEBUG"])


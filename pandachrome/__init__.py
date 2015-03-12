from flask import Flask
from flask import session
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/linstead/Dropbox/apps/pandachrome/sqlite.db'

db = SQLAlchemy(app)
from pandachrome import views, models

#@app.before_first_request
#def setup_user():
#    app.logger.debug('in setup')
#    user = models.User.query.filter_by(username='ciaron').first()
#    session['site_title'] = user.site_title

#@app.before_first_request
#def parse_settings():
#    # TODO figure out session expiration/force expiration
#    with open(os.path.join(dbox, settings)) as f:
#        for line in f:
#            if line[0] != '#':
#                line.split(':')
#                session[line.split(':')[0]] = line.split(':')[1].strip()
#
#    f.close()
#

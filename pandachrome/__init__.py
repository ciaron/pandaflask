from flask import Flask
from flask import session
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/linstead/src/pandachrome.flask/pandachrome/sqlite.db'

cache = Cache(app,config={'CACHE_TYPE': 'simple'})
db = SQLAlchemy(app)
from pandachrome import views, models

#galleries = {}
#
#@app.before_first_request
#def get_galleries():
#    from dropbox import client
#    app.logger.debug('in get_galleries (from Dropbox)')
#    mimes = ['image/png', 'image/jpeg']
#    # my access_token (for user 'ciaron')
#    tk='8d6DYpbiA1IAAAAAAAApQDDC7Yobyv6WYumChXSkp3Zt3OVBwHSKplhSFnWdsr0g'
#    api=client.DropboxClient(tk)
#
#    r=api.metadata('/')
#
#    for i in r['contents']:
#        if i['is_dir'] == True:
#            p = i['path']
#
#            galleries[p] = []
#            g = api.metadata(p)
#            for img in g['contents']:
#                if img['mime_type'] in mimes:
#                    galleries[p].append(api.media(img['path'])['url'])
#

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

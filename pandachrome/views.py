import os
from flask import Flask
from flask import render_template
from flask import session
from flask import current_app, Blueprint
from . import models
from . import app

api = Blueprint('api', __name__)

#settings = 'settings'
#dbox = '/home/linstead/Dropbox/apps/pandachrome/static/pandadrop'
#allowed_exts=['.jpg', '.jpeg', '.png', 'tif', 'tiff']
#prefix_sep = '_' # the character by which we separate the prefix from the gallery name

#app = Flask(__name__)
#app.secret_key='\xbdHV\xe1/[O\x7fD\xef\xb5\xf3\xe4\xa6\xac\x0c\xdaT\xc5\x83\x1c\xfb\xd1\xc3'

dbox = app.config["DBOX"]
prefix_sep = app.config["PREFIX_SEP"]
settings = app.config["SETTINGS"]
allowed_exts = app.config["ALLOWED_EXTS"]
DEBUG=app.config["DEBUG"]

def is_image(f):

    if DEBUG:
        app.logger.debug(f.lower())

    if os.path.splitext(f.lower())[1] in allowed_exts:
        return True
    else:
        return False

def get_image_title(f):
    """
    get the image title from an image filename of the form
    01_IMG_2914_[This is the title].JPG

    Test cases:

    01_DSC_111.jpg
    02_DSC_111_[TITLE_TEST].jpg
    [03].jpg
    [04].jpg
    [04_TEST].jpg
    05_DSC.jpg
    [05].jpg
    150227_123401_0002[The Title].png
    150303_150010_0002.PNG
    1.jpg
    [5].jpg
    a.jpg
    B.jpg
    [TITLE_TEST].jpg
    z.jpg

    """
    
    if f.find('[') == -1 or f.find(']') == -1:
        # no matching square brackets in filename
        return os.path.splitext(os.path.split(f)[1])[0]
    else:
        return f[f.find("[")+1:f.find("]")]

def get_gallery_folders():
    # return a list of gallery folder names, i.e. including prefixes
    galleries = [d for d in os.listdir(dbox) if os.path.isdir(os.path.join(dbox, d))]
    return sorted(galleries)

def get_gallery_names():
    # return a list of gallery names, (i.e. folders without prefixes), sorted by prefix
    galleries = [d for d in os.listdir(dbox) if os.path.isdir(os.path.join(dbox, d))]
    return [g.split(prefix_sep)[-1] for g in sorted(galleries)]

def get_gallery_images(gallery_id):
    # return a sorted list of all the images for a specific gallery
    files = []

    # galleries are indexed from 1 for nicer URLs
    gallery_folders = get_gallery_folders()
    g = gallery_folders[gallery_id-1]

    fs = [os.path.join(g, f) for f in os.listdir(os.path.join(dbox, g)) if is_image(os.path.join(dbox, g, f))]

    if DEBUG:
        app.logger.debug(sorted(fs))

    for f in sorted(fs):
        files.append({'path': f, 'title': get_image_title(f)})
    return files

@app.before_first_request
def setup_user():
    user = User.query.filter_by(username='ciaron').first()
    session['SITE_TITLE'] = user.site_title

#@app.before_first_request
def parse_settings():
    # TODO figure out session expiration/force expiration
    with open(os.path.join(dbox, settings)) as f:
        for line in f:
            if line[0] != '#':
                line.split(':')
                session[line.split(':')[0]] = line.split(':')[1].strip()

    f.close()

@api.route('/')
def index():
    galleries = get_gallery_names();
    parse_settings()

    if DEBUG:
        app.logger.debug(galleries)

    return render_template('main.html', galleries=galleries)

# show a gallery, starting at first image (if none specified) or at image number 'image_id'
@api.route('/<int:gallery_id>/', defaults={'image_id':None})
@api.route('/<int:gallery_id>/<int:image_id>/')
def gallery(gallery_id, image_id=None):

#    if 'title' not in session:
#        parse_settings()
    # TODO every time for now...
    # let's get persistent data (eg. site title) from database.
    parse_settings()

    g_images = get_gallery_images(gallery_id)

    if DEBUG:
        app.logger.debug(g_images)

    return render_template('gallery.html', gallery_id=gallery_id, image_id=image_id, g_images=g_images, DBOXROOT=dbox)

#if __name__ == '__main__':
#    api.run(debug=True)

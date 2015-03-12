import os
from flask import Flask
from flask import render_template
from flask import request, session, flash, redirect, url_for
from pandachrome import app
from pandachrome.models import User

dbox = os.path.join(os.getcwd(), app.config["DBOX"])
prefix_sep = app.config["PREFIX_SEP"]
settings = app.config["SETTINGS"]
allowed_exts = app.config["ALLOWED_EXTS"]
DEBUG = app.config["DEBUG"]

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

@app.route('/')
def index():
    galleries = get_gallery_names();
    
    if DEBUG:
        app.logger.debug(galleries)

    return render_template('main.html', galleries=galleries)

# show a gallery, starting at first image (if none specified) or at image number 'image_id'
@app.route('/<int:gallery_id>/', defaults={'image_id':None})
@app.route('/<int:gallery_id>/<int:image_id>/')
def gallery(gallery_id, image_id=None):

    g_images = get_gallery_images(gallery_id)

    if DEBUG:
        app.logger.debug(g_images)

    return render_template('gallery.html', gallery_id=gallery_id, image_id=image_id, g_images=g_images, DBOXROOT=dbox)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        if username:
#            db = get_db()
#            db.execute('INSERT OR IGNORE INTO users (username) VALUES (?)', [username])
#            db.commit()
            session['user'] = username
            flash('You were logged in')
            return redirect(url_for('index'))
        else:
            flash("You must provide a username")
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)

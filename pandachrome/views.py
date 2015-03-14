import os
from flask import Flask
from flask import render_template
from flask import request, session, flash, redirect, url_for
from pandachrome import app, cache
from pandachrome.models import User

dbox = os.path.join(os.getcwd(), app.config["DBOX"])
prefix_sep = app.config["PREFIX_SEP"]
settings = app.config["SETTINGS"]
allowed_exts = app.config["ALLOWED_EXTS"]
DEBUG = app.config["DEBUG"]

@cache.cached(timeout=3600, key_prefix='all_galleries') # dropbox media timeout is 4 hours, 14400 secs; share timeout 1 hour (3600s)
def get_galleries():
    galleries = {}

    from dropbox import client
    mimes = ['image/png', 'image/jpeg']

    # my access_token (for user 'ciaron')
    tk='8d6DYpbiA1IAAAAAAAApQDDC7Yobyv6WYumChXSkp3Zt3OVBwHSKplhSFnWdsr0g'
    api=client.DropboxClient(tk)

    r=api.metadata('/')

    for i in r['contents']:
        if i['is_dir'] == True:
            p = i['path']

            galleries[p] = []
            g = api.metadata(p)
            for img in g['contents']:
                if img['mime_type'] in mimes:
                    #u = api.media(img['path'])['url']

                    u = api.share(img['path'], short_url=False)['url']
                    if u.find('?dl=') == -1:
                        u = u+'?dl=1'
                    else:
                        u = u.replace('?dl=0', '?dl=1')
                    galleries[p].append(u)
    return galleries

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

#def get_gallery_folders():
#    # return a list of gallery folder names, i.e. including prefixes
#    galleries = [d for d in os.listdir(dbox) if os.path.isdir(os.path.join(dbox, d))]
#    return sorted(galleries)

def get_gallery_names():
    # return a list of gallery names, (i.e. folders without prefixes), sorted by prefix
    cached_galleries = get_galleries().keys()
    return cached_galleries

def get_gallery_images(gallery_id):

    cached_galleries = get_galleries()
    files = cached_galleries[cached_galleries.keys()[gallery_id-1]]
    return files

#    # return a sorted list of all the images for a specific gallery
#    files = []
#
#    # galleries are indexed from 1 for nicer URLs
#    gallery_folders = get_gallery_folders()
#    g = gallery_folders[gallery_id-1]
#
#    fs = [os.path.join(g, f) for f in os.listdir(os.path.join(dbox, g)) if is_image(os.path.join(dbox, g, f))]
#
#    if DEBUG:
#        app.logger.debug(sorted(fs))
#
#    for f in sorted(fs):
#        files.append({'path': f, 'title': get_image_title(f)})
#    return files
#
@app.route('/')
def index():
    galleries = sorted(get_gallery_names())
    
    if DEBUG:
        app.logger.debug(galleries)

    return render_template('main.html', galleries=galleries)

# show a gallery, starting at first image (if none specified) or at image number 'image_id'
@app.route('/<int:gallery_id>/', defaults={'image_id':None})
@app.route('/<int:gallery_id>/<int:image_id>/')
def gallery(gallery_id, image_id=None):

    # currently a list of dropbox URLs
    g_images = get_gallery_images(gallery_id-1)
    app.logger.debug(g_images)

    # make a dict: {'title': 'url',...} 
    # ORDER?

    #if DEBUG:
    #    app.logger.debug(g_images)

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

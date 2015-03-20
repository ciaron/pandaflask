import os
import urllib
from collections import OrderedDict
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

def check_cache():
    # if something changed on the Dropbox side, we invalidate our cache
    # cursor = user.cursor
    #if api.delta(cursor)['entries'] != []:
    #    # delete the cache
    #    cache.clear()
    pass

# dropbox media timeout is 4 hours, 14400 secs; share timeout 1 hour (3600s)
@cache.memoize(timeout=3600) 
def get_galleries():

    # TODO: only get the top-level galleries!
    # move image url fetching to (cached) functions that get called
    # when the view is called!!

    galleries = []

    from dropbox import client
#    mimes = ['image/png', 'image/jpeg']

    # my access_token (for user 'ciaron')
    tk='8d6DYpbiA1IAAAAAAAApQDDC7Yobyv6WYumChXSkp3Zt3OVBwHSKplhSFnWdsr0g'
    api=client.DropboxClient(tk)

    r=api.metadata('/')

    for i in r['contents']:
        if i['is_dir'] == True:
            p = i['path']

            galleries.append(p)
#            g = api.metadata(p)
#            for img in g['contents']:
#                if img['mime_type'] in mimes:
#                    #u = api.media(img['path'])['url']
#
#                    u = api.share(img['path'], short_url=False)['url']
#                    if u.find('?dl=') == -1:
#                        u = u+'?dl=1'
#                    else:
#                        u = u.replace('?dl=0', '?dl=1')
#                    galleries[p].append(urllib.unquote(u))

    #return OrderedDict(sorted(galleries.items(), key=lambda t: t[0]))
    return sorted(galleries)

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
    01+IMG_2914_[This is the title].JPG

    """
    if f.find('[') == -1 or f.find(']') == -1:
        # no matching square brackets in filename
        x = os.path.splitext(os.path.split(f)[1])[0]
    else:
        x = f[f.find("[")+1:f.find("]")]

    try: 
        x = x.split(prefix_sep)[1]
    except:
        pass

    return x

def get_gallery_names():
    # return a list of gallery names, (i.e. folders without prefixes), sorted by prefix
    check_cache()
    #cached_galleries = get_galleries().keys()
    cached_galleries = get_galleries()
    return [ g.split(prefix_sep)[-1].lstrip('/') for g in cached_galleries ]

def get_name(s):
    return os.path.splitext(os.path.split(s)[1])[0]

@cache.memoize(timeout=3600) 
def get_gallery_images(gallery_id):

    app.logger.debug('in get_gallery_images')

    # TODO: SORT ORDER!!!!
    # { url : (path, title) }

    mimes = ['image/png', 'image/jpeg']
    tk='8d6DYpbiA1IAAAAAAAApQDDC7Yobyv6WYumChXSkp3Zt3OVBwHSKplhSFnWdsr0g'
    from dropbox import client
    api=client.DropboxClient(tk)

    images = {}
    check_cache() # does nothing for now
    g = api.metadata(get_galleries()[gallery_id-1])
    for img in g['contents']:
        if img['mime_type'] in mimes:
            u = api.share(img['path'], short_url=False)['url']
            if u.find('?dl=') == -1:
                u = u+'?dl=1'
            else:
                u = u.replace('?dl=0', '?dl=1')
            #images.append(urllib.unquote(u))
            images[(urllib.unquote(u))] = (img['path'], get_image_title(img['path']))

    #files = cached_galleries[cached_galleries.keys()[gallery_id-1]]

    #for i in files:
    #    images[get_image_title(i)] = i

    return OrderedDict(sorted(images.items(), key=lambda t:get_name(t[1][0])))
    #return OrderedDict(sorted(images.items(), key=get_name))
    #return sorted(images)

@app.route('/')
def index():
    galleries = get_gallery_names()
    
    #if DEBUG:
    #    app.logger.debug(galleries)

    return render_template('main.html', galleries=galleries)

# show a gallery, starting at first image (if none specified) or at image number 'image_id'
@app.route('/<int:gallery_id>/', defaults={'image_id':None})
@app.route('/<int:gallery_id>/<int:image_id>/')
def gallery(gallery_id, image_id=None):

    # currently a list of dropbox URLs
    g_images = get_gallery_images(gallery_id)
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

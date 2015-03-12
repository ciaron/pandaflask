from pandachrome import db

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), unique=True)
    access_token = db.Column(db.String(128), unique=True)
    site_title = db.Column(db.String(128))

    def __init__(self, username, email, site_title):
        self.username = username
        self.email = email
        self.site_title = site_title

    def __repr__(self):
        return '<User %r>' % self.username

import pprint
from dropbox import client

pp = pprint.PrettyPrinter(indent=4)
mimes = ['image/png', 'image/jpeg']
# my access_token (for user 'ciaron')
tk='8d6DYpbiA1IAAAAAAAApQDDC7Yobyv6WYumChXSkp3Zt3OVBwHSKplhSFnWdsr0g'
api=client.DropboxClient(tk)

r=api.metadata('/')
#pp.pprint(r)
galleries = {}

for i in r['contents']:
    if i['is_dir'] == True:
        p = i['path']

        print p
        print(api.metadata(p))
        
#        galleries[p] = []
#        g = api.metadata(p)
#        for img in g['contents']:
#            if img['mime_type'] in mimes:
#                galleries[p].append(api.media(img['path'])['url'])

#pp.pprint(galleries)
#pp.pprint(api.delta(cursor='AAGwwrIqBAwFxeI6Hr4dpgdR6xxY1n3axBrOsXzTAecutolsJ5SNCvTKMc-4NoQMcwXZ42hjNVJBkAnVf0ONleCX0rsv_8HHv3VRSqIYzfPWWg'))
"""
# pass the cursor. 
# if no changes:

{   u'cursor': u'AAGvffcUJqIb16ZTU7qbSpxigVn2gTlDMR4eGJ1p9CUkUgRQHZqFOrcXTAGNkJcvNztX9-zGblNDhwuFxBmbktbo8O6xlHwiMohV-AEXNYve1w',
    u'entries': [],
    u'has_more': False,
    u'reset': False}

otherwise:

{   u'cursor': u'AAFv4vGW23D5NvRyaA5atMMGcv_xwcZ0FhdWm7NN5IxlouCkyiCXEAwWHZmngTbvQ5-aiaDv-5lLanXgCh1iSLWHIWNYQrq6PTeY22rRY0y5qA',
    u'entries': [   [u'/02_gallery3/01_dsc_111.jpg', None],
                    [   u'/02_gallery3/01_dsc_123.jpg',
                        {   u'bytes': 740580,
                            u'client_mtime': u'Thu, 12 Mar 2015 13:55:39 +0000',
                            u'icon': u'page_white_picture',
                            u'is_dir': False,
                            u'mime_type': u'image/jpeg',
                            u'modified': u'Fri, 13 Mar 2015 15:33:46 +0000',
                            u'path': u'/02_gallery3/01_DSC_123.jpg',
                            u'rev': u'1af32d59524',
                            u'revision': 431,
                            u'root': u'app_folder',
                            u'size': u'723.2 KB',
                            u'thumb_exists': True}]],
    u'has_more': False,
    u'reset': False}


"""
"""
r = api.metadata(galleries['/02_gallery3'])
#pp.pprint(r)
for i in r['contents']:
    if i['mime_type'] == 'image/png':
        print api.media(r['contents'][0]['path'])
        # {u'url': u'https://dl.dropboxusercontent.com/1/view/ga5sd7xpdnsbgov/apps/pandachrome/01_gallery1/150218_182055_0464.png', u'expires': u'Fri, 13 Mar 2015 15:56:24 +0000'}
        #print cl.media(r['path'])
"""

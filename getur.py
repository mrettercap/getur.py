#!/usr/bin/env python3
import httplib2
import json
import os
import argparse

auth_headers = {'Authorization':'Client-ID 37d87caf158e8a4'}
cache_dir    = os.path.join(os.path.expanduser("~"),'.getur_cache')

class Image:
    '''our image class, deals with all image-related activities'''
    def __init__(self, imgur_id, imgur_type='image'):
        self.imgur_id = imgur_id
        self.imgur_type = imgur_type
        # Set our cache directory
        self.h = httplib2.Http(cache_dir)
        self.response,self.content = self.h.request('https://api.imgur.com/3/{0}/{1}'
                                  .format(self.imgur_type, self.imgur_id),
                                  headers=auth_headers)

    def validate(self):
        '''validates whether the image exists on imgur'''
        if self.response["status"] == '200':
            return True
        else:
            return False

    def download(self, subreddit):
        '''downloads the image'''
        js = json.loads(self.content.decode('utf-8'))

        # make the subreddit dir. if it already exists,
        # don't warn us; it's nbd.
        try:
            os.makedirs(subreddit)
        except:
            pass
      
        # FYI: \x1b[A positions the cursor 'up' one line.
        # \x1b[K deletes everything to the right of the cursor.
        print("\x1b[A{0} (1/1)\x1b[K".format(js['data']['id']))
        response, content = self.h.request(js['data']['link'])
        with open(os.path.join(subreddit, '{}.jpg'.format(js['data']['id'])), 'wb') as f:
                f.write(content)
        return "\x1b[ADownloaded 1 file.\x1b[K"

# extend Image
class Album(Image):
    def __init__(self, imgur_id):
        super(Album,self).__init__(imgur_id, imgur_type='album')
    def download(self,subreddit):
        js = json.loads(self.content.decode('utf-8'))
        try:
            os.makedirs(os.path.join(subreddit,js['data']['id']))
        except:
            pass

        count = 0
        for i in js['data']['images']:
            count += 1
            if i['animated'] == True:
                img_fn = "{0}-{1}.gif".format(format(count,'02d'),i['id'])
            else:
                img_fn = "{0}-{1}.jpg".format(format(count,'02d'),i['id'])
            print("\x1b[A{0} ({1}/{2})\x1b[K".format(i['id'],count,js['data']['images_count']))
            response, content = self.h.request(i['link'])
            with open(os.path.join(subreddit,self.imgur_id,img_fn), 'wb') as f:
                f.write(content)
        return "\x1b[ADownloaded {} files.\x1b[K".format(count) 

class Imgur:
    '''main class for dealing with imgur downloads'''

    def __init__(self, imgur_id, subreddit):
        self.imgur_id = imgur_id
        self.subreddit = subreddit
        
    def fetch(self):
        if Album(self.imgur_id).validate() == False:
            if Image(self.imgur_id).validate() == False:
                raise Exception("No such item exists!")
            else:
                print("Found image {}".format(self.imgur_id))
                print(Image(self.imgur_id).download(self.subreddit))
        else:
            print("Found album {}".format(self.imgur_id))
            print(Album(self.imgur_id).download(self.subreddit))


parser = argparse.ArgumentParser()
parser.add_argument("theid", help="the imgur ID of the item")
parser.add_argument("subreddit", help="the subreddit the item is from")
args = parser.parse_args()

Imgur(args.theid,args.subreddit).fetch()

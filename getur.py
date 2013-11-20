#!/usr/bin/env python3
import httplib2
import json
import os
import argparse

auth_headers = {'Authorization':'Client-ID 37d87caf158e8a4'}

# Image class
class Image:
    '''our image class, deals with all image-related activities'''
    def __init__(self, imgur_id, imgur_type='image'):
        self.imgur_id = imgur_id
        self.imgur_type = imgur_type
        # Set our cache directory
        self.h = httplib2.Http('.cache')
        self.resp,self.content = self.h.request('https://api.imgur.com/3/{0}/{1}'
                                  .format(self.imgur_type, self.imgur_id),
                                  headers=auth_headers)

    def validate(self):
        '''validates whether the image exists on imgur'''
        if self.resp["status"] == '200':
            return True
        else:
            return False

    def download(self, subreddit):
        '''downloads the image'''
        # turn the content we grabbed in the __init__
        # function into a json dictionary
        js = json.loads(self.content.decode('utf-8'))

        # make the subreddit dir. if it already exists,
        # don't warn us; it's nbd.
        try:
            os.makedirs(subreddit)
        except:
            pass
       
        print("\x1b[A{0} (1/1)\x1b[K".format(js['data']['id']))
        # now grab the image, pull it into a variable
        resp, content = self.h.request(js['data']['link'])
        # open the image locally with format:
        # {subreddit}/{count-with-leading-zero}-{id}.jpg
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
            resp, content = self.h.request(i['link'])
            with open(os.path.join(subreddit,self.imgur_id,img_fn), 'wb') as f:
                f.write(content)
        return "\x1b[ADownloaded {0} files.\x1b[K".format(count) 

class Imgur:
    '''grab files'''

    def __init__(self, imgur_id, subreddit, imgurType=None):
        self.imgur_id = imgur_id
        self.subreddit = subreddit
        self.imgurType = imgurType
        self.count = 0
        
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

# Tests:
# ------

# 1. Invalid imgur ID raises exception (4-6 letters/numbers)
# 2. Blank arg raises exception
# 3. If it doesn't exist, raises exception
# 4. Make sure if it can't be reached (network fail), raises exception


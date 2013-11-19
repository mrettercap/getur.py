import httplib2
import json
import os

class Fetch:
    '''grab files'''

    def __init__(self, album, subreddit, forceOverwrite=False):
        self.album = album
        self.subreddit = subreddit
        self.forceOverwrite = forceOverwrite
        self.count = 0
        h = httplib2.Http('.cache')
        print("Making connection with imgur for album {}".format(album))
        resp, content = h.request("https://api.imgur.com/3/album/{}".format(album), headers={'Authorization':'Client-ID 37d87caf158e8a4'})
        print("Album found. Parsing data")
        self.js = json.loads(content.decode('utf-8'))
        self.images_count = self.js["data"]["images_count"]

        try:
            os.makedirs(os.path.join(self.subreddit,self.js["data"]["id"]))
        except:
            if self.forceOverwrite == False:
                raise Exception("This album has already been downloaded!")
            else:
                pass

        print("Grabbing {1} total images for album {0}:".format(self.album, self.images_count))

        # 1. make a connection with imgur. 
        #   a. find out whether it's an image or an album
        #   b. set images_count accordingly
        #   c. announce "downloading image_name"
        #   d. download.

    def __iter__(self):
        return self

    def __next__(self):
        self.count += 1
        if self.count > self.images_count:
            raise StopIteration

        h = httplib2.Http('.cache')
        resp, content = h.request(self.js["data"]["images"][self.count - 1]["link"])


        with open(os.path.join(
                                self.subreddit,
                                self.js["data"]["id"],
                                "{0}-{1}.jpg".format(format(self.count, '02d'), # leading zero
                                                     self.js["data"]["images"][self.count - 1]["id"])
                              ),
                  "wb") as f:
            f.write(content)

        return self.count, self.js["data"]["images"][self.count - 1]["id"]


# h = httplib2.Http('.cache')
# resp, content = h.request("https://api.imgur.com/3/album/Nu83J", headers={'Authorization':'Client-ID 37d87caf158e8a4'})
# js = json.loads(content.decode('utf-8'))

# title:     js["data"]["title"]
# desc:      js["data"]["description"]
# no_images: js["data"]["images_count"]
# cover:     js["data"]["cover"]

# images:

# for i in js["data"]["images"]:
#        print(i["id"]) # etc

# if i["id"]["animated"] == True:
#       i.ext = ".gif"

# Downloads for:
# --------------

# Albums
# Images
# Then users

# Tests:
# ------

# 1. Invalid imgur ID raises exception (4-6 letters/numbers)
# 2. Blank arg raises exception
# 3. If it doesn't exist, raises exception
# 4. Make sure if it can't be reached (network fail), raises exception


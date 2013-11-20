getur.py
========

getur.py is an Imgur album/image downloader written in—you guessed it—python.

## Usage

./getur.py {imgur id} {subreddit}

The script will figure out if the id you're referencing is an image or album, then download it 
locally to `{subreddit}/{id}.jpg` or `{subreddit}/{album id}/{image id}.jpg` for albums.

If the image is animated, it'll save it as a gif.

It also caches in order to avoid putting too much strain on imgur's servers; in the unlikely
event that you want to re-download stuff, it can just pull the images/data from there. Thanks, httplib2.

The cache directory is ~/.getur_cache.

That's really all there is to it. 
Enjoy.

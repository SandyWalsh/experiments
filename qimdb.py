"""
To mount, let's say \\Workstation\ShareName
sudo apt-get install samba4-clients
Find IP address for Stuff: nmblookup Workstation
sudo apt-get install smbfs
sudo mkdir /mnt/ShareName
sudo mount -t cifs 192.168.2.xxx:ShareName /mnt/ShareName
"""

try:
    from local_settings import SHARE_NAME
except ImportError:
    SHARE_NAME = r"/mnt/ShareName"

import os
import imdb


def dump(movie, fields, commas = False):
    first = True
    for f in fields:
        if f in movie:
            if first:
                print "%s: " % (f.upper(),),
            else:
                print "(",
            if type(movie[f]) == list:
                for i in movie[f] [ 0 : min(5, len(movie[f])) ]:
                    if commas:
                        print "%s," % (i,),
                    else:
                        print "%s" % (i,),
            else:
                print "%s" % (movie[f],),
            if not first:
                print ")",
            first = False
    if not first:
        print


svr = imdb.IMDb()
for root, dirs, files in os.walk(SHARE_NAME):
    print root
    for file in files:
        copy = file
        lower = file.lower()
        if file[-4:] != '.avi':
            continue

        file = file[:-4]  # remove .avi
        file = file.replace(" ", ".")
        parts = file.split(".")
        search = " ".join(parts)

        print "Was: %s now '%s'" % (copy, search)
        for movie in svr.search_movie(search)[:1]:
            svr.update(movie)
            dump(movie, ['title', 'year', 'rating'])
            dump(movie, ['genre'])
            dump(movie, ['plot'])
            dump(movie, ['cast'], commas = True)
            print "-------------------------------------------------------------------"

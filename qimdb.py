import os
import imdb
svr = imdb.IMDb()

def dump(movie, fields, commas = False):
    first = True
    for f in fields:
        if movie.has_key(f):
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

root = r"\\stuff\sandbox\Movies"
for root, dirs, files in os.walk(root):
    print root
    for file in files:
        copy = file
        lower = file.lower()
        if file[-4:] != '.avi':
            continue

        file = file[:-4] # remove .avi
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

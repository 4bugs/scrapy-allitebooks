# -*- encoding: utf-8 -*-
import pymongo
import os
import time

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "itbooks"



if __name__ == '__main__':
    conn = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
    db = conn[MONGODB_DB]
    urls = list(db.books.find({}, {'download_links': 1, '_id': 0}))
    for url in urls:
        os.system('wget -U NoSuchBrowser/1.0 -P /Users/wangqi/tmp//books %s' % url["download_links"])
        db.books.update({"download_links": url["download_links"]},{"$set":{"has_download":1}})
        time.sleep(5)
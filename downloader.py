#!/usr/bin/env python
#-*- coding:utf-8 -*-

from tweepy import *
import urllib
import os
import datetime
import argparse

parser = argparse.ArgumentParser(description='Twitter Userstream Image Downloader')
parser.add_argument('--config', '-c', required=True, type=str,
                    help='config path')
parser.add_argument('--list', '-l', required=True, type=str,
                    help='user list path')
args = parser.parse_args()

def get_oauth():
    with open(args.config, 'rb') as f:
        data = f.read()
    f.close()
    lines = data.split('\n')
    consumer_key = lines[0]
    consumer_secret = lines[1]
    access_key = lines[2]
    access_secret = lines[3]
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return auth

def get_userlist():
    with open(args.list, 'rb') as l:
        lines = l.readlines()
    l.close()
    return lines

class StreamListener(StreamListener):
    def on_status(self, status):
        if status.entities.has_key('media') and not status.entities.has_key('retweeted_status'):
            for line in lines:
                 if line.find(status.author.screen_name) >= 0:
                    medias = status.entities['media']
                    m =  medias[0]
                    media_url = m['media_url']
                    print media_url
                    now = datetime.datetime.now()
                    time = now.strftime("%H%M%S")
                    filedir = './download/{}'.format(status.author.screen_name)
                    try:
                        os.makedirs(filedir)
                    except OSError:
                        pass
                    filename = os.path.join(filedir, '{}.jpg'.format(status.id))
                    print filename
                    try:
                        urllib.urlretrieve(media_url, filename)
                    except IOError:
                        print "保存に失敗しました"

auth = get_oauth()
lines = get_userlist()
stream = Stream(auth, StreamListener(), secure = True)
print "Start Streaming!"
try:
    os.makedirs('./download')
except OSError:
    pass
stream.userstream()

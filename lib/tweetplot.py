import sys
import tweepy
from lib.tweetkeys import *
from wand.image import Image
import platform
import os
## for second version, because problems with Wand on OSX
#from svglib.svglib import svg2rlg
#from reportlab.graphics import renderPM
import subprocess               # May want to use subprocess32 instead


print("invoking TWEEEEEETING")
print(platform.system())

# ## get ourselves the image we need (convert svg to jpg)
# with Image(filename=sys.argv[2]) as img:
#     img.format = 'jpeg'
#     img.save(filename='out.jpg')


# pi = tweepy.API(auth) 
# tweet = sys.argv[1] # some text + 
# image_path = "tmp/out2.jpg" # jpg created above or in plotrender.py
# print(image_path)
# # to attach the media file 
# #status = 
# api.update_with_media(image_path, tweet)  
# # api.update_status(status = tweet) 

##### using wand on OSX renders erroneously, 

# def convertSVGtoTweet(svg, tweettext):
#     with Image(filename=svg) as img:
#         img.format = 'jpeg'
#         img.save(filename='tweet.jpg')
#         # authentication 
#         auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
#         auth.set_access_token(access_token, access_token_secret) 
#         api = tweepy.API(auth) 
#         tweet = tweettext
#         image_path = "tweet.jpg" # jpg created above
#         print(image_path, tweet)
#         # to attach the medicd /Ap  a file 
#         #status = 
#         api.update_with_media(image_path, tweet)  
#         # api.update_status(status = tweet) 




def TweetImgTxt(image_path, tweettext):

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    auth.set_access_token(access_token, access_token_secret) 
    api = tweepy.API(auth) 
    print (dir(api))
    tweet = tweettext
    # image_path = "tweet.png" # png created above
    print(image_path, tweet)
    # to attach the media file 
    #status = 

    ## deprecated method
    #api.update_with_media(image_path, tweet)  
    # api.update_status(status = tweet) 
    ## new method
    file=open(image_path, 'rb')
    media_id = api.media_upload(filename=image_path, file=file)
    # api.update_with_updatemedia(file, tweet)  
    # api.update_status(status = tweet) 

    print(media_id)
    #https://docs.tweepy.org/en/v4.0.0/api.html#tweepy.API.simple_upload
    api.update_status(tweet, media_ids=[media_id.media_id_string])
    #https://stackoverflow.com/questions/37050450/tweepy-python-library-media-ids-parameter-is-invalid-and-tweet-must-not-have
    
def convertSVGtoTweet(svg, tweettext):
    print(svg)
    pltfrm = platform.system()
    if (pltfrm == 'Darwin'):
        cmd_list = [ '/Applications/Inkscape.app/Contents/MacOS/inkscape','--export-filename=tweet.png', svg ]
        p = subprocess.Popen( cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        out, err = p.communicate()
        if p.returncode:
            raise Exception( 'Inkscape error: ' + (err or '?')  )
    else:
        # cmd_list = [ '/usr/bin/inkscape','--export-filename=tweet.png', svg ]
        with Image(filename=svg) as img:
            img.format = 'png'
            img.save(filename='tweet.png')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    auth.set_access_token(access_token, access_token_secret) 
    api = tweepy.API(auth) 
    tweet = tweettext
    image_path = "tweet.png" # png created above
    print(image_path, tweet)
    # to attach the media file 
    #status = 

    ## deprecated method
    #api.update_with_media(image_path, tweet)  
    # api.update_status(status = tweet) 
    ## new method
    file=open(image_path, 'rb')
    media_id = api.media_upload(filename=image_path, file=file)

    # media_id = api.simple_upload(filename=image_path, file=file)
    print(media_id)
    #https://docs.tweepy.org/en/v4.0.0/api.html#tweepy.API.simple_upload
    api.update_status(tweet, media_ids=[media_id.media_id_string])
    #https://stackoverflow.com/questions/37050450/tweepy-python-library-media-ids-parameter-is-invalid-and-tweet-must-not-have
    
    
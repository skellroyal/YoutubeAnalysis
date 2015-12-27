# videos/views.py

from datetime import datetime
from django.shortcuts import render
from trips.models import Post



#------doris------
import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from oauth2client import tools
from django.shortcuts import render_to_response
from django.http.response import HttpResponse


CLIENT_SECRETS = os.path.join(
    os.path.dirname(__file__), 'client_secret_776396627823-fueq6uu5eu6imjgvfhefta69o0d6fp5f.apps.googleusercontent.com.json')

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"



# Authorize the request and store authorization credentials.
def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS, scope=YOUTUBE_READ_WRITE_SCOPE)

    storage = Storage("ooo-oauth2.json")
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        flags = tools.argparser.parse_args(args=[])
        credentials = run_flow(flow, storage, flags)

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http()))

def hello_world(request):
    return render(request, 'hello_world.html', {'current_time': datetime.now()})

def home(request):
    # get all the posts
    post_list = Post.objects.all()
    return render(request,
                  'home.html',
                  {'post_list': post_list})

def post_detail(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'post.html', {'post': post})

def login(request):
    return render(request,
                  'login.html')
     
def call_youtube_api(request):
    
    youtube = get_authenticated_service()
    
    myRating = "like"
    ss = list_video_localizations(request, youtube, myRating)
    return render(request, 'hello_world.html', {'current_time': ss})

# Call the API's videos.list method to list the existing video localizations.
def list_video_localizations(request, youtube, myRating):
    results = youtube.videos().list(part="snippet,localizations", myRating=myRating).execute()
    result_items = results["items"]

#   localized = results["items"][0]["snippet"]["localized"]

    s = ""
    for item in result_items:
        title = item["snippet"]["localized"]["title"]
        description = item["snippet"]["localized"]["description"]
        s += "Video title is '%s' and description is '%s'" % (title, description) + "\n"

    return s
#     now = datetime.now()
# 
#     html = "<html><body>It is now %s.</body></html>" % now
# #     return HttpResponse(html)
#     return HttpResponse('Hi')






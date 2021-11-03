from flask import Flask
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi

# define a variable to hold you app
app = Flask(__name__)

# define your resource endpoints
app.route('/')
def index_page():
    return "Hello world"

app.route('/time', methods=['GET'])
def get_time():
    return str(datetime.datetime.now())

def youtube_vedio_transcript_english(vedio_id:str):
    transcript_en = YouTubeTranscriptApi.get_transcript(vedio_id , languages=['en'])
    transcript = ""
    for item in transcript_en:
        transcript += item["text"]
    return transcript


# server the app when this file is run
if __name__ == '__main__':
    app.run()

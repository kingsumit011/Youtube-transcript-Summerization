from html.entities import html5
from flask import Flask
from flask import request
from requests.sessions import Request
from transformers import T5ForConditionalGeneration, T5Tokenizer

from youtube_transcript_api import YouTubeTranscriptApi


# define a variable to hold you app
app = Flask(__name__)

# define your resource endpoints
@app.route('/')
def index_page():
    html =  '''\
    <!DOCTYPE html>
    <html>
        <head>
        </head>
    <body>
        '''+"Hello World" + '''
    </body>
    </html>'''
    return html

@app.route('/api/summarize', methods=['GET'])
def main():
    vedio_id = request.args.get('youtube_vid')
    transcript = youtube_vedio_transcript_english(vedio_id)
    
    html =  '''\
    <!DOCTYPE html>
    <html>
        <head>
        </head>
    <body>
        '''+transcript + '''
    </body>
    </html>'''
    return html;

def youtube_vedio_transcript_english(vedio_id:str):
    transcript_en = YouTubeTranscriptApi.get_transcript(vedio_id , languages=['en-US'])
    transcript = ""
    for item in transcript_en:
        transcript += item["text"]
    return transcript_summarization(transcript)

def transcript_summarization(transcript:str):

    # initialize the model architecture and weights
    model = T5ForConditionalGeneration.from_pretrained("t5-large")
    # initialize the model tokenizer
    tokenizer = T5Tokenizer.from_pretrained("t5-large")  
    # encode the text into tensor of integers using the appropriate tokenizer
    inputs = tokenizer.encode("summarize: " + transcript, return_tensors="pt", max_length=1024, truncation=True)
    # generate the summarization output
    outputs = model.generate(
    inputs, 
    max_length=250, 
    min_length=100, 
    length_penalty=2.0, 
    num_beams=4, 
    early_stopping=True)

    summary =tokenizer.decode(outputs[0])
    return summary

# server the app when this file is run
if __name__ == '__main__':
    app.run()

from flask import Flask
from datetime import datetime
from transformers import T5ForConditionalGeneration, T5Tokenizer

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

from flask import Flask, request
import json
import re
import newspaper
from gtts import gTTS
import hashlib
from langdetect import detect

app = Flask(__name__, static_url_path='/static', static_folder='static/')

def check_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

@app.route("/")
def homepage():
    return "Welcome to BrowsEar!"

@app.route("/text/") 
def gettext():
    form = """
<form action="/text2speech/" name="textform" method="post">
    <textarea id="textforspeech" class="text" cols="86" rows ="20" name="textforspeech"></textarea>
<br><br>
   <input type="submit" value="Talk to me" class="submitButton">
</form>
    """
    return form

@app.route("/text2speech/", methods=["POST"])
def text2speech():
    the_text = request.form['textforspeech']
    text_lang = detect(the_text)
    try:
        tts = gTTS(the_text, lang=text_lang)
    except:
        return "Sorry. The language of the article is not supported!"

    m = hashlib.md5()
    m.update(bytes(the_text, "utf-8"))
    mp3filename = m.hexdigest()
    mp3savepath = f"./static/{mp3filename}.mp3"
    tts.save(mp3savepath)
    mp3url = f"{request.url_root}static/{mp3filename}.mp3"
    mp3href=f'<a href="{mp3url}"> Listen here! </a>'
    mp3player=f'<video controls="" autoplay="" name="media"><source src="{mp3url}" type="audio/mpeg"></video>'
    return f"{mp3player} <br> <br> <a href='/text/'> Listen other text </a>" 

@app.route("/listen/<path:articleurl>")
def listen(articleurl):
    if not check_url(articleurl):
        return "Error: Wrong url!", 400
    article = newspaper.Article(articleurl)
    article.download()
    article.parse()
    text_lang = detect(article.text)
    try:
        tts = gTTS(article.text, lang=text_lang)
    except:
        return "Sorry. The language of the article is not supported!"
    # generate filename
    m = hashlib.md5()
    m.update(bytes(articleurl, "utf-8"))
    mp3filename = m.hexdigest()
    mp3savepath = f"./static/{mp3filename}.mp3"
    tts.save(mp3savepath)
    mp3url = f"{request.url_root}static/{mp3filename}.mp3"
    mp3href=f'<a href="{mp3url}"> Listen here! </a>'
    #mp3player=f'<audio controls> <source src="{mp3savepath}" type="audio/mpeg">  </audio>'
    mp3player=f'<video controls="" autoplay="" name="media"><source src="{mp3url}" type="audio/mpeg"></video>'
    return f"Article url: <a href='{articleurl}'> {article.title} </a> <br> <br> Article text: {article.text}  <br> <br> Listen here: <br> {mp3player}" 


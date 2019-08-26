# browsear

## Browser for your ears

**This program should ease people into reading news/information from the web.**

The motivation

Reading information from a web page could be a hard (even dangerous) process (disabled people, bad web desing, lazy people, reckless drivers). 

What if you don't use your eyeballs but your ears isntead?

Is the world going to become better (and safe) place? 

Yes.

----

**How to use it**

(you will need python3 and virtualenv installed on your system)

$ git clone git@github.com:ctmnz/browsear.git
$ cd browsear
$ python3 -m virtualenv ./browsearenv
$ . ./browsearenv/bin/activate
$ pip install -r requirements.txt
$ ./start.sh
.
.

In your browser:
 - Open http://localhost:5000/text/
 - Copy and paste your text in the form
or 
 - Open http://localhost:5000/listen/<url> (i.e. http://localhost:5000/listen/https://edition.cnn.com/2019/07/21/europe/bulgaria-hack-tax-intl/index.html ) 
 - Wait a little bit (sorry)
 - Click the play button below.



The amazing technology used in this project:
- Flask (https://palletsprojects.com/p/flask/)
- gTTS (https://pypi.org/project/gTTS/)
- newspapper (https://pypi.org/project/newspaper3k/)
- langdetect (https://pypi.org/project/langdetect/)
- hashlib (https://docs.python.org/3/library/hashlib.html)



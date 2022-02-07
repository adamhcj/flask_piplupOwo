from flask import Flask
from threading import Thread
import time
import random


app = Flask('')

@app.route('/')
def home():
  htmlstring = "<p>Hello world!</p>"
  htmlstring += "<a href='/test'>test page</a><br>"
  htmlstring += "<a href='/random/'>generate random number page</a>"
  return htmlstring

@app.route('/test/')
def test():
  return "hello test page!<br><a href='/'>back to home page</a>"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()

def background_task():
  count = 0
  while True:
    print(count)
    count += 1
    time.sleep(5)

def run_bg_task():
  bgthread = Thread(target=background_task)
  bgthread.start()


@app.route('/random/<number>/')
def randompage(number):
  print("random page visited")
  random_number = random.randint(0, int(number))
  returnjson = {"number" : random_number}
  htmlstring = returnjson

  return htmlstring

@app.route('/random/')
def randomstartpage():
  htmlstring = f"<p>random start page</p>"
  htmlstring += "<a href='/'>back to home page</a>"
  htmlstring += "<h1>generate a random number from 0 to :</h1><ul>"

  for i in range(0, 101, 10):
    htmlstring += f"<li><a href='{i}'>{i}</a></li>"

  htmlstring += "</ul>"

  return htmlstring



keep_alive()
run_bg_task()
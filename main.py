from flask import Flask
from threading import Thread
import time

app = Flask('')

@app.route('/')
def home():
    return "Hello. I am alive!"

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

keep_alive()

bgthread = Thread(target=background_task)
bgthread.start()
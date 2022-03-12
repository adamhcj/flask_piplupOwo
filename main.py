from flask import Flask, redirect, request, jsonify
from threading import Thread
import time
import random
import os
import requests


import base64
import json


CLIENTID = os.environ['CLIENTID']
CLIENTSECRET = os.environ['CLIENTSECRET']
CLIENTSID = CLIENTID + ":" + CLIENTSECRET

app = Flask('')

@app.route('/')
def home():
  htmlstring = "<p>Hello world!</p>"
  htmlstring += "<a href='/test'>test page</a><br>"
  htmlstring += "<a href='/random/'>generate random number page</a>"
  htmlstring += "<br><a href='/dbstest/login'>test dbs sandbox api</a>"
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

@app.route('/dbstest/login')
def dbslogin():
  redirecturi = f'https://flaskpiplupOwo.adamho2.repl.co/dbstest'
  
  authurl = f'https://www.dbs.com/sandbox/api/sg/v1/oauth/authorize?client_id={CLIENTID}&scope=Read&response_type=code&redirect_uri={redirecturi}&state=0399&login_page=card'

  return f"<h2>Hello, welcome to piplupOwo's replit web application, demonstrating DBS Developers OAuth 2.0 api (learning for school project use)</h2><br><h3>Please select Singapore IC and key in '1234' for all fields when logging in: </h3><a href='{authurl}'>login to dbs portal</a>"

  


@app.route('/dbstest')
def dbstest():


  def get_access_token(accesscode): #get access token with access code
    global portnumber
    global encodedclientsid
    redirecturi = f'https://flaskpiplupOwo.adamho2.repl.co/dbstest'

    encodedclientsid = base64.b64encode(CLIENTSID.encode()).decode()

    headers = {
    'Authorization': f'Basic {encodedclientsid}',
    }

    data = {
    'code': f'{accesscode}',
    'redirect_uri': f'{redirecturi}',
    'grant_type': 'token'
    }

    response = requests.post('https://www.dbs.com/sandbox/api/sg/v1/oauth/tokens', headers=headers, data=data)
    print(response.text)
    return response.text #access token
  #---------------------------------------------
  global accesstoken
  global party_id
  global accesscode
  global CLIENTID

  
  
  htmlstring = "<br><h1>Send top up amount, then 2FA will be prompted, click send sms and key in any 6 digits </h1>\
  <form action='/dbstest/pay' method='get'>\
      top up amount: <input type='number' name='amount' min='1' value='10'> <button type='submit' onclick='alert(`are you sure you want to pay $\{document.getElementbyId('amountid')\}?`)'>pay</button>\
  </form>\
  <br><br><br>"

  accesscode = request.args.get('code')
  response = get_access_token(accesscode)



  #htmlstring += response
  response = json.loads(response)

  accesstoken = response['access_token']

  return f"<br>"+htmlstring
  

@app.route('/dbstest/pay')
def pay():

  global accesstoken
  global party_id
  global accesscode
  global amount
  global CLIENTID
  
  amount = request.args.get('amount')

  
  redirect2uri = "https://flaskpiplupowo.adamho2.repl.co/dbstest/paid"

  htmlstring = f"<script>window.location.href='https://www.dbs.com/sandbox/api/sg/v1/access/authorize?code={accesscode}&elevationPref=3&client_id={CLIENTID}&state=0399&redirect_uri={redirect2uri}';</script>"






  return htmlstring


@app.route('/dbstest/paid')
def paid():
  global amount
  try:
    htmlstring = f"congrats! you successfully topped up ${amount}"
  except:
    return redirect("/", code=302)
  return htmlstring + "<br><a href='/dbstest/login'>back to login page</a>"

  
keep_alive()
run_bg_task()
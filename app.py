from flask import Flask, render_template, request, redirect
import pandas as pd
import bokeh
import requests
import simplejson

app = Flask(__name__)

@app.route('/')
def home_page():
  return render_template('home_page.html')

# @app.route('/about')
# def about():
#   return render_template('about.html')

# @app.route('/hello_page_test')
# def hello_world():
#     return 'Hello world'

@app.route('/user_input')
def user_input():
    return render_template('userinfo_lulu.html')

if __name__ == '__main__':
  app.run(port=33507)

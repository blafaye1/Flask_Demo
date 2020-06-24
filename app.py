from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/hello_page_test')
def hello_world():
    return 'Hello world'

if __name__ == '__main__':
  app.run(port=33507)

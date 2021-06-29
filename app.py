#export FLASK_APP=hellp (but if you use app.py, FLASK figures it out automatically for us)
#export FLASK_ENV=development
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', name="Jason")


@app.route('/your-url', methods=['GET', 'POST'])
# def yoho(): # name don't have to match
def your_url(): # name don't have to match
    if request.method == 'POST':
        return render_template('your_url.html', code=request.form['code'], url=request.form['url'])
    elif request.method == 'GET':
        return "GET method"
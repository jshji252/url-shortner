#export FLASK_APP=hellp (but if you use app.py, FLASK figures it out automatically for us)
#export FLASK_ENV=development
from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "2n10d9qcwnrpdsjklf@_=1891@"

@app.route('/')
def home():
    return render_template('home.html', codes = session.keys())


@app.route('/your-url', methods=['GET', 'POST'])
# def yoho(): # name don't have to match
def your_url(): # name don't have to match
    if request.method == 'POST':
        # Save data into JSON
        urls = {}
        code = request.form['code']

        ## Check if the codename exists already
        if os.path.exists('urls.json'):
            with open('urls.json', 'r') as url_file:
                urls = json.load(url_file)
        if code in urls.keys(): # Check existence
            flash("That Short Name has already been taken. Please choose another name.")
            return redirect(url_for('home'))

        if 'url' in request.form.keys():
            urls[code] = {'url' : request.form['url']}
        else:
            f = request.files['file']
            full_name = code + secure_filename(f.filename)
            f.save('/Users/mraji/Documents/Developer/url-shortner/static/user_files/' + full_name)
            urls[code] = {'file' : full_name}

        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            session[code] = True
        return render_template('your_url.html', code=request.form['code'])
    elif request.method == 'GET':
        # If user is accessing this page via GET method, send him back to the home page
        # return redirect('/') # this is less robus because what we actually want to do is to call 'home' function.  
        return redirect(url_for('home')) # so let's do that, but need url_for library

@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json', 'r') as url_file:
            urls = json.load(url_file)
        if code in urls.keys():
            if 'url' in urls[code].keys():
                return redirect(urls[code]['url'])
            else:
                # display the picture
                # serve static file
                return redirect(url_for('static', filename='user_files/'+urls[code]['file']))
    return abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))
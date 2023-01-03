import validators
import os
import secrets
from flask import Flask, render_template, request, flash, redirect, url_for, abort
from .db import URLRepository

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_urlsafe(16))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=["GET"])
def urls():
    records = URLRepository().find_all()
    return render_template('sites.html', records=records)


@app.route('/urls/<int:id>', methods=['GET'])
def show(id):
    repo = URLRepository()
    record = repo.find(id)

    if not record:
        return abort(404)
    
    return render_template('page.html', record=record)


@app.route('/urls', methods=['POST'])
def post_urls():
    data = request.form.get('url')
    
    if not data:
        flash('URL is required', 'danger')
        return redirect('/')


    if not validators.url(data) or len(data) > 255:
        flash('URL is not valid, please enter valid url', 'danger')
        return redirect('/')

    try:
        repo = URLRepository()
        found_record = repo.find_by_name(data)
        if found_record:
            flash("URL already exists", 'info')
            return redirect(url_for('show', id=found_record.get('id')))

        return redirect(url_for('show', id = repo.save({'name': data})))
    except Exception as ex:
        return abort(500, ex)

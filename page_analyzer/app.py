import validators
import os
import requests
import secrets
from flask import Flask, \
    render_template, request, flash, redirect, url_for, abort
from .db import URLRepository, URLCheckRepository
from .page import get_page_data

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", secrets.token_urlsafe(16))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/urls", methods=["GET"])
def urls():
    records = URLRepository().find_all()
    return render_template("sites.html", records=records)


@app.route("/urls/<int:id>/checks", methods=["POST"])
def url_check(id):
    site_for_check = URLRepository().find(id)

    if not site_for_check:
        abort(404)
    try:
        response = requests.get(site_for_check.get("name"))
        response.raise_for_status()
        repo = URLCheckRepository()
        res = {"status_code": response.status_code}
        res.update(get_page_data(response.content.decode()))
        repo.save(id, **res)
        flash("Страница успешно проверена", "success")
    except Exception as ex:
        flash("Произошла ошибка при проверке", "danger")

    return redirect(url_for("show", id=id))


@app.route("/urls/<int:id>", methods=["GET"])
def show(id):
    repo = URLRepository()
    record = repo.find(id)

    if not record:
        return abort(404)

    checks = URLCheckRepository().find_all(id)

    return render_template("page.html", record=record, checks=checks)


@app.route("/urls", methods=["POST"])
def post_urls():
    data = request.form.get("url")

    if not data or not validators.url(data) or len(data) > 255:
        flash("Некорректный URL", "danger")
        return redirect("/", 422)

    try:
        repo = URLRepository()
        found_record = repo.find_by_name(data)
        if found_record:
            flash("Страница уже существует", "info")
            return redirect(url_for("show", id=found_record.get("id")))
        
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for("show", id=repo.save({"name": data})))
    except Exception as ex:
        flash(f"Error while store url {ex=}", "danger")
        return redirect("/")

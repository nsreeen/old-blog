from flask import render_template
from app import app, pages

@app.route('/')
def index():
    posts = [page for page in pages]
    return render_template('index.html', pages=posts)

@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)

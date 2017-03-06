from flask import render_template
from app import app, pages
from werkzeug.contrib.atom import AtomFeed

@app.route('/')
def index():
    posts = [page for page in pages]
    return render_template('index.html', pages=posts)

@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)

def entries_list(pages, limit=None):
    entries = [p for p in pages]
    entries = sorted(entries, reverse=True)
    return entries[:limit]

@app.route('/blog/atom.xml')
def blog_feed():
    feed = AtomFeed('Recent Blog Postings',
                    feed_url='/blog/atom.xml')#+url_for('blog_feed'),
                    #url='/')
    blog_list = entries_list(pages, 10)
    for b in blog_list:
        feed.add(b.meta['title'],
                 content_type='html',
                 url='blog/'+b.path+'.html',
                 updated=b.meta['date'])
                 #published=b.meta['published'])
    return feed.get_response()

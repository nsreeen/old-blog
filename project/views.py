from flask import render_template
from app import app, pages
from werkzeug.contrib.atom import AtomFeed

@app.route('/')
def index():
    posts = [p for p in pages if p.meta['type']  == 'post']
    ordered_posts = sorted(posts, reverse=True,
     key=lambda p: p.meta['date'])
    return render_template('index.html', pages=ordered_posts)

@app.route('/notes')
def notes():
    posts = [p for p in pages if p.meta['type']  == 'note' and p.meta['publish'] == 'true']
    ordered_posts = sorted(posts, reverse=True,
     key=lambda p: p.meta['date'])
    return render_template('notes.html', pages=ordered_posts)

@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)

def blog_post_list(pages, limit=None):
    entries = [p for p in pages if p.meta['type']  == 'post'] # CHECK THIS LATER!!!
    entries = sorted(entries, reverse=True)
    return entries[:limit]

@app.route('/atom.xml')
def blog_feed():
    feed = AtomFeed('Recent Blog Postings',
                    feed_url='/atom.xml')#+url_for('blog_feed'),
                    #url='/')
    blog_list = blog_post_list(pages, 10)
    for b in blog_list:
        feed.add(b.meta['title'],
                 content_type='html',
                 url=b.path,
                 updated=b.meta['date'])
                 #published=b.meta['published'])
    return feed.get_response()

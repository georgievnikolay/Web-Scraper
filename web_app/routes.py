from web_app import app
from flask import render_template
from web_app.data import get_posts_on_page


@app.route('/')
@app.route('/index')
@app.route('/home')
def home():
    return "Under construction."


@app.route('/page/<int:page_num>')
def page(page_num):
    return render_template('page.html', posts=get_posts_on_page(page_num, 5))


@app.route('/post/<int:post_id>')
def single_post(post_id):
    return f"Post {post_id}"
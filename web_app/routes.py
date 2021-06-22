from web_app import app
from flask import render_template, redirect, url_for
from web_app.data import blogs


@app.route('/')
@app.route('/index')
@app.route('/home')
def home():
    existing_blogs = [name for name in blogs.keys() if blogs[name] is not None]
    return render_template('home.html', blogs=existing_blogs)

@app.route('/<blog>/page/<int:page_num>')
def page(blog, page_num):
    if blog not in blogs.keys() or blogs[blog] is None:
        return redirect(url_for('not_found'))

    posts = blogs[blog].get_posts_on_page(page_num)
    return render_template('page.html', posts=posts, curr_page=page_num, 
                            num_pages=blogs[blog].get_num_pages(), blog=blog)

@app.route('/<blog>/post/<int:post_id>')
def single_post(blog, post_id):
    if blog not in blogs.keys() or blogs[blog] is None:
        return redirect(url_for('not_found'))

    return render_template('post.html', post=blogs[blog].get_post(post_id), 
                            num_posts=blogs[blog].get_num_posts(), blog=blog)

@app.route('/404')
def not_found():
    return "404 Not Found"
    
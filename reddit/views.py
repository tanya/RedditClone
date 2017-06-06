from reddit import app, db, lm
from flask import request, render_template, redirect, url_for
from models import *
from datetime import datetime
from flask_login import login_user, current_user, login_required, logout_user
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import desc

@lm.user_loader
def load_user(id):
    return UserDB.query.get(int(id))


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        if request.form.get('login_or_signup') == 'signup':
            user = UserDB.query.filter_by(email=email).first()
            if user is not None:
                return render_template('error.html', error='This email already exists!')
            user = UserDB.query.filter_by(username=username).first()
            if user is not None:
                return render_template('error.html', error='This username already exists!')
            user = UserDB(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            login_user(user,True)
            return redirect(url_for('home'))
        else: #login
            user = UserDB.query.filter_by(username=username,password=password).first()
            if user is None:
                return render_template('error.html', error='We can\'t find a username with that password')
            login_user(user,True)
            return redirect(url_for('home'))


@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        top_posts = PostDB.query.order_by(desc(PostDB.num_likes)).limit(50).all()
        if top_posts is None:
            return render_template('header.html')
        return render_template('header.html', posts=top_posts)


@app.route('/hello')
def index():
    return "Hello, world!"


@app.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    if request.method == 'GET':
        return render_template('write.html')
    if request.method == 'POST':
        #userBob = UserDB(email="bob@bob",username="Bob",password="bobbo")
        new_tag = request.form.get('tag')
        title = request.form.get('title')
        content = request.form.get('content')
        print(str(title + " " + content + " "))
        time = datetime.now()
        post = PostDB(title=title, author=current_user.username, content=content, num_likes=0, time=time)
        db.session.add(post)

        tag = TagDB(name=new_tag)
        db.session.add(tag)
        db.session.commit()

        #connect the post and the tag
        existing_tag = TagDB.query.filter_by(name=new_tag).first()
        if existing_tag is None:
            post_tag = PostTagDB(tag_id=tag.id, post_id=post.id)
        else:
            post_tag = PostTagDB(tag_id=existing_tag.id, post_id=post.id)

        db.session.add(post_tag)
        db.session.commit()
        return redirect(url_for('home'))

@app.route('/tags/<tag_name>', methods=['GET'])
def tag(tag_name):
    tag = TagDB.query.filter_by(name=tag_name).first()
    if tag is None:
        return render_template('error.html', error='Tag does not exist yet.');
    post_tags = PostTagDB.query.filter_by(tag_id=tag.id).all()
    #map applies a function to a list
    post_ids = map(lambda x: x.post_id, post_tags) #list of post_ids for posts queried above
    posts = map(lambda x: PostDB.query.filter_by(id=x).first(), post_ids)
    return render_template('tags.html',tag=tag_name,posts=posts)

@app.route('/posts/<post_id>', methods=['GET','POST'])
def post(post_id):
    if request.method == 'GET':
        post = PostDB.query.filter_by(id=post_id).first()
        if post is None:
            return render_template('error.html', error='Looks like that post doesn\'t exist.')
        comments = CommentDB.query.filter_by(post_id=post_id).all()
        return render_template('post.html', post=post, comments=comments)
    if request.method == 'POST':
        #content of comment
        content = request.form.get('content')
        author = current_user.username
        time = datetime.now()
        comment = CommentDB(content=content, author=author, post_id=post_id, num_likes=0, time=time)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('post',post_id=post_id))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


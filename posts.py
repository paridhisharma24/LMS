from flask import render_template, redirect, flash, request, abort, Blueprint, url_for
from flask_login import current_user, login_required
from __init__ import db
from models import Post, Reply
from models import User
from forms import PostForm, ReplyForm
from datetime import date
today = date.today
posts = Blueprint('posts', __name__)

@posts.route('/Dforum', methods=['GET', 'POST']) 
def Dforum(): 
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    form = ReplyForm()
    replies = Reply.query.all()
    return render_template('posts.html', title = 'Home', 
	posts = posts, votes = 0, form = form, replies = replies, page = page)

@posts.route("/my_posts")
def my_posts():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(user_id = current_user.user_id)\
		.order_by(Post.date_posted.desc())\
		.paginate(page=page, per_page=5)
	type = 'post'
	return render_template('posts.html', title = 'My Posts', posts = posts
		, type = type)
@posts.route("/post/new", methods=['GET', 'POST'])
def new_post():
	form= PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content = form.content.data, author = current_user)
		db.session.add(post)
		db.session.commit()
		#flash('Your post has been created', 'success')
		return redirect(url_for('posts.Dforum'))
	return render_template('create_post.html', title = 'New Post',
		form = form, legend = 'New Post', action = 'Create')

@posts.route("/post/<int:post_id>/update", methods = ['GET','POST'])

def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		#flash('Your post has been updated', 'success')
		return redirect(url_for('posts.my_posts'))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title = 'Update Post',
		form = form, legend = 'New Post', action = 'Update')

@posts.route("/post/<int:post_id>/delete", methods = ['GET','POST'])
def delete_post(post_id):
	print(post_id)
	print(Post.query.get_or_404(post_id))
	replies= Reply.query.filter_by(post_id=post_id).all()
	print(replies)
	for reply in replies:
		if (reply.post_id==post_id):
			db.session.delete(reply)
			db.session.commit()
	post = Post.query.get_or_404(post_id)
	db.session.delete(post)
	db.session.commit()
	#flash('Your post has been deleted', 'info')
	return redirect(url_for('posts.my_posts'))
			
		
	
	    

   
	
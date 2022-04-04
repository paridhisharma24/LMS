
from flask import render_template, redirect, flash, request, abort, Blueprint, url_for
from flask_login import current_user, login_required
from __init__ import db
from models import Post, Reply
from forms import PostForm, ReplyForm

posts = Blueprint('posts', __name__)


@posts.route('/Dforum', methods=['GET', 'POST']) 
def Dforum(): 
   
    course_id=request.args.get('course_id')
   
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(course_id=course_id)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=3)
    form = ReplyForm()
    replies = Reply.query.all()
    return render_template('posts.html', title = 'Home',course_id=course_id,
	posts = posts, form = form, replies = replies, page = page)

@posts.route("/my_posts")
def my_posts():
    course_id= request.args.get('course_id')
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(user_id = current_user.user_id,course_id=course_id)\
		.order_by(Post.date_posted.desc())\
		.paginate(page=page, per_page=3)
    type = 'post'
    return render_template('posts.html', title = 'My Posts', posts = posts
		, type = type,course_id=course_id)

		

@posts.route("/post/new", methods=['GET', 'POST'])
def new_post():
    form= PostForm()
    course_id=request.args.get('course_id')
    print(course_id)
    if form.validate_on_submit():
        post= Post(title=form.title.data, content = form.content.data, author = current_user,course_id=course_id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.Dforum',course_id=course_id))
    return render_template('createpost.html', title = 'New Post',
		form = form, legend = 'New Post', action = 'Create',course_id=course_id)
    
	

@posts.route("/post/<int:post_id>/update", methods = ['GET','POST'])

def update_post(post_id):
    course_id=request.args.get('course_id')
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data+" (updated)"
        db.session.commit()
        return redirect(url_for('posts.my_posts',course_id=course_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('createpost.html', title = 'Update Post',
		form = form, legend = 'New Post', action = 'Update',course_id=course_id)
		
		
		
		
		
@posts.route("/post/<int:post_id>/delete", methods = ['GET','POST'])
def delete_post(post_id):
    course_id=request.args.get('course_id')
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
    return redirect(url_for('posts.my_posts',course_id=course_id))
	
@posts.route("/search", methods = ['GET','POST'])
def search():
    course_id=request.args.get('course_id')
    print("search")
    print(course_id)
    tag = request.form.get("Search")
    search = "%{}%".format(tag)
    page = request.args.get('page', 1, type=int)
    postss= Post.query.filter_by(course_id=course_id).filter(Post.title.like(search))\
		.order_by(Post.date_posted.desc())\
		.paginate(page=page, per_page=3)
    form = ReplyForm()
    replies = Reply.query.all()
    return render_template('posts.html', title = 'Home',course_id=course_id,
	posts = postss, form = form, replies = replies, page = page)
    
	
	
	
		
			
			
	
	
	
	
	
			
		
	
	    

   
	
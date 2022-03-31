from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_required, login_user, current_user, logout_user
from __init__ import db
from models import Post, Reply
from forms import ReplyForm

replies = Blueprint('replies', __name__)

@replies.route("/reply/<int:post_id>/<int:user_id>/<int:page>", methods = ['POST'])
def reply_post(post_id, user_id, page):
    course_id=request.args.get('course_id')
    reply = Reply.query.filter_by(user_id = user_id, post_id = post_id).first()
    form = ReplyForm()
    if form.validate_on_submit():
        post = Post.query.get_or_404(post_id)
        reply = Reply(content = form.content.data, user = current_user, post = post)
        db.session.add(reply)
        db.session.commit()
        flash('You have successfully replied!', 'success')
    return redirect(url_for('posts.Dforum', page = page,course_id=course_id))
	
	
    
    
	
		
		
		
		
		
	
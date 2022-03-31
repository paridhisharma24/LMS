from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
	title = StringField('Subject', validators = [DataRequired()])
	content = TextAreaField('Content', validators = [DataRequired()])
	submit = SubmitField('Post')
    
class ReplyForm(FlaskForm):
	content = TextAreaField('Content', validators = [DataRequired()])
	submit = SubmitField('Reply')
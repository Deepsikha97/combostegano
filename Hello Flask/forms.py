from flask_wtf import Form
from wtforms import validators,TextField, TextAreaField, SubmitField, PasswordField, BooleanField,FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email,ValidationError

def length_check(form,field):
    if len(field.data) == 0:
        raise ValidationError('Fields should not be null')

class SenderForm(Form):
    name= TextField('Name', validators= [DataRequired(), length_check])
    key = TextField('Key', validators= [DataRequired(),length_check])
    message = TextField('Message', validators= [ DataRequired(), length_check])
    image = FileField(u'Image File',[validators.regexp(u'^[^/\\]\.jpg$')])
    submit = SubmitField('Submit')
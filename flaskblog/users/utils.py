import os #module to get whether image file is png or jpg
import secrets
from flask_mail import Message
from flaskblog import mail
from flask import url_for, current_app
#from PIL import Image #to resize the image before we save it

def save_picture(form_picture):
    random_hex = secrets.token_hex(8) #changing the name of the image file that user had given in their system cos it might collide
    _, f_ext = os.path.splitext(form_picture.filename) # the _ is to throw away the f_name variable cos its useless for us
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # output_size = (125,125)         #resizing
    # i = Image.open(form_picture) 
    # i.thumbnail(output_size)
    # i.save(picture_path)

    form_picture.save(picture_path)

    return picture_fn #fn = filename

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                 sender = os.environ.get('EMAIL_USER'), 
                 recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)} 

If you did not make this request then simply ignore this email and no changes will be made. ''' #external thing is for absolute address not relative address like we've been giving so far

    mail.send(msg)
'''
Code that will allow us to uplaod pictures
This script will handle pictures in the backend
'''

import os
from PIL import Image
from flask import url_for, current_app

def add_profile_picture(picture_upload, username):

    filename = picture_upload.filename
    # somepic.jpg -> 'somepic' . 'jpg' -> This will split by '.' and grab the last element, in our case the extension
    extension_type = filename.split('.')[-1]
    # 'username.jpg'
    storage_filename = str(username)+'.'+extension_type

    filepath = os.path.join(current_app.root_path, 'static/profile_pictures', storage_filename)

    output_size = (200, 200)

    pic = Image.open(picture_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    # username.png
    return storage_filename
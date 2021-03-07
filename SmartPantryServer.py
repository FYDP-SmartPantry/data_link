from flask import Flask, flash, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

from flask import send_from_directory
from food_prediction import food_dect
from PIL import Image


app = Flask(__name__)
UPLOAD_FOLDER = ''
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['jpg','png','jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/predict', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            image_url = url_for('uploaded_file', filename=filename)
            re,po = food_dect(os.path.join(app.config['UPLOAD_FOLDER'], filename),"resnet50_weights_tf_dim_ordering_tf_kernels.h5")
            #re = ''
            return '''<h1>The prediction is: {} {}</h1><img src="{}" height = "85" width="200"/>'''.format(re,po, image_url)


    return '''
    <!doctype html>
    <title>Upload new Photo</title>
    <h1>Upload a jpg/png/jpeg of vegetable or fruit</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
   app.run(host='0.0.0.0',debug=True)

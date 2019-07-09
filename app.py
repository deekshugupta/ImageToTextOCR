from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
from PIL import Image
from pytesseract import image_to_string

app = Flask(__name__)
# UPLOAD_FOLDER =  'uploads'
UPLOAD_FOLDER = os.path.join('static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
src_path = "static/"



def get_string(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite(src_path + "removed_noise.png", img)
    cv2.imwrite(src_path + "gettext.jpg", img)
    result = pytesseract.image_to_string(Image.open(src_path + "gettext.jpg"))
    return result

@app.route("/")
def main():
    return render_template('index.html',name = '', filename='')

@app.route('/upload', methods = ['POST'])
def upload_file():
   filename = ' '
   result1 = ' '
   if request.method == 'POST':
      f = request.files['file']
      print(f.filename)
      if f :
            filename = secure_filename(f.filename)
            f.save(os.path.join('static', filename))
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            result1 = get_string(src_path + f.filename)
            # return redirect(url_for('uploaded_file',filename=filename))
            return render_template('index.html', name = result1, filename=full_filename)
      else :
           return render_template('index.html', name = '', filename='')



if __name__ == "__main__":
    app.run()
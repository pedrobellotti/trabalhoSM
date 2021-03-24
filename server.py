import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import datetime
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(APP_ROOT, '/Videos')
app.config['UPLOAD_FOLDER'] = target

@app.route('/')
def uploader_file():
   return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      dt = datetime.now()
      filename = dt.strftime("%d-%b-%YT%H:%M:%S")
      f.save(secure_filename(filename))
      return 'Arquivo enviado com sucesso!'

if __name__ == '__main__':
   app.run(debug = True)
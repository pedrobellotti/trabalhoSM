import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import datetime
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './Videos/'

@app.route('/')
def uploader_file():
   return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      dt = datetime.now()
      timestamp = dt.strftime("%d-%b-%YT%H:%M:%S")
      name = f.filename.rsplit('.', 1)[0].lower()
      filename = secure_filename(name + "-" + timestamp)
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return 'Arquivo enviado com sucesso!'

if __name__ == '__main__':
   app.run(debug = True)